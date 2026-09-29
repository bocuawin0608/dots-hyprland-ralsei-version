#!/usr/bin/env python3
"""RALSEI OS – Lyric Synchronisation Daemon

Listens to the active MPRIS player, finds a matching *.lrc* file in
~/.lyrics, and streams timed lyric JSON objects to a UNIX socket
(or stdout). Automatically fetches missing lyrics from lrclib.net.

Dependencies:
    pip install dbus-next
"""

from __future__ import annotations

import asyncio
import json
import re
import signal
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Tuple

from dbus_next.aio import MessageBus
from dbus_next import Message, MessageType, BusType

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
LYRIC_DIR = Path.home() / ".lyrics"
SOCKET_PATH = Path.home() / ".config/quickshell/ii/lyrics_socket"

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def parse_lrc(text: str) -> List[Tuple[int, str]]:
    """Convert an LRC file to a sorted list of (timestamp_ms, lyric) tuples.
    Supports multiple timestamps per line.
    """
    timestamp_re = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\]")
    entries: List[Tuple[int, str]] = []
    for line in text.splitlines():
        stamps = timestamp_re.findall(line)
        lyric = timestamp_re.sub("", line).strip()
        if not lyric:
            continue
        for minute, sec in stamps:
            ms = int(float(minute) * 60_000 + float(sec) * 1_000)
            entries.append((ms, lyric))
    entries.sort(key=lambda t: t[0])
    return entries


def locate_lrc(artist: str, title: str) -> Path | None:
    """Simple heuristic to find a matching .lrc file."""
    if not LYRIC_DIR.is_dir():
        return None
    candidates = [
        f"{artist} - {title}.lrc",
        f"{title}.lrc",
        f"{artist}_{title}.lrc",
        f"{artist}-{title}.lrc",
    ]
    for name in candidates:
        p = LYRIC_DIR / name
        if p.is_file():
            return p
    return None


def clean_query(title: str, artist: str = "") -> str:
    """Sanitize MPRIS data to improve LRCLIB search results."""
    def brutal_clean(text: str) -> str:
        if not text: return ""

        # 1. Truncate EVERYTHING after trigger characters
        text = re.split(r'\||\bft\.?\b|\bfeat\.?\b|\s+x\s+', text, flags=re.IGNORECASE)[0]

        # 2. Remove ALL text inside (), [], <>, 【】 (leaving no empty brackets)
        text = re.sub(r'[\(\[<【].*?[\)\]>】]', '', text)

        # 3. Strip ALL emojis (covers standard Unicode ranges for pictographs)
        text = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27BF\u2300-\u23FF\u2B50\u2B55]', '', text)

        # 4. Delete the blacklisted words
        blacklist = [r'\bremix\b', r'\bnightcore\b', r'\bversion\b',
                     r'\bofficial\b', r'\bvideo\b', r'\brock ai\b', r'\bcover\b']
        for word in blacklist:
            text = re.sub(word, '', text, flags=re.IGNORECASE)

        # 5. Cleanup: Strip hyphens, replace double spaces, strip whitespace
        text = re.sub(r'-', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    t = brutal_clean(title)
    a = brutal_clean(artist)

    query = f"{t} {a}".strip()

    # De-duplicate words while keeping order (helpful for LRCLIB fuzzy search)
    seen = set()
    cleaned = []
    for word in query.split():
        if word.lower() not in seen:
            seen.add(word.lower())
            cleaned.append(word)

    return " ".join(cleaned)


async def fetch_lrclib(query: str) -> str | None:
    """Asynchronously search lrclib.net and return syncedLyrics if available."""
    if not query:
        return None

    def _do_request():
        url = f"https://lrclib.net/api/search?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'RalseiOS-LyricDaemon/1.0'})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f"[lyric-daemon] LRCLIB API error: {e}", file=sys.stderr)
            return None

    loop = asyncio.get_event_loop()
    # Run the blocking HTTP request in a thread so we don't stall DBus/Socket
    data = await loop.run_in_executor(None, _do_request)

    if not data or not isinstance(data, list):
        return None

    for item in data:
        if item.get("syncedLyrics"):
            return item["syncedLyrics"]

    return None

# ----------------------------------------------------------------------
# Low-level DBus helpers (bypass fragile ProxyInterface naming)
# ----------------------------------------------------------------------


async def dbus_list_names(bus: MessageBus) -> list[str]:
    reply = await bus.call(
        Message(
            destination="org.freedesktop.DBus",
            path="/org/freedesktop/DBus",
            interface="org.freedesktop.DBus",
            member="ListNames",
        )
    )
    if reply.message_type == MessageType.ERROR:
        raise RuntimeError(f"ListNames failed: {reply.body}")
    return reply.body[0]


async def dbus_get_property(
    bus: MessageBus, service: str, path: str, iface: str, prop: str
):
    reply = await bus.call(
        Message(
            destination=service,
            path=path,
            interface="org.freedesktop.DBus.Properties",
            member="Get",
            signature="ss",
            body=[iface, prop],
        )
    )
    if reply.message_type == MessageType.ERROR:
        raise RuntimeError(f"Get({iface}.{prop}) failed: {reply.body}")
    return reply.body[0].value


async def dbus_get_all_properties(
    bus: MessageBus, service: str, path: str, iface: str
) -> dict:
    reply = await bus.call(
        Message(
            destination=service,
            path=path,
            interface="org.freedesktop.DBus.Properties",
            member="GetAll",
            signature="s",
            body=[iface],
        )
    )
    if reply.message_type == MessageType.ERROR:
        raise RuntimeError(f"GetAll({iface}) failed: {reply.body}")
    return {k: v.value for k, v in reply.body[0].items()}


# ----------------------------------------------------------------------
# Daemon core
# ----------------------------------------------------------------------

PLAYER_IFACE = "org.mpris.MediaPlayer2.Player"
PROPERTIES_IFACE = "org.freedesktop.DBus.Properties"
MPRIS_PATH = "/org/mpris/MediaPlayer2"


class LyricDaemon:
    """Manages DBus listening, lyric timing and output."""

    def __init__(self) -> None:
        self.bus: MessageBus | None = None
        self.player_service: str | None = None
        self.current_track_id: str | None = None
        self.lyrics: List[Tuple[int, str]] = []
        self.next_index: int = 0
        self.start_position_ms: int = 0
        self.start_monotonic: float = 0.0
        self._next_timer: asyncio.TimerHandle | None = None
        self._download_task: asyncio.Task | None = None

        # Socket server
        self._socket_server: asyncio.AbstractServer | None = None
        self._client_writer: asyncio.StreamWriter | None = None

    # ------------------------------------------------------------------
    # DBus initialisation
    # ------------------------------------------------------------------
    async def init_bus(self) -> None:
        self.bus = await MessageBus(bus_type=BusType.SESSION).connect()

        names = await dbus_list_names(self.bus)
        for n in sorted(names):
            if n.startswith("org.mpris.MediaPlayer2."):
                self.player_service = n
                break

        if not self.player_service:
            raise RuntimeError(
                "No MPRIS player found on the session bus.\n"
                "Start a media player (Spotify, VLC, Firefox, etc.) first."
            )

        print(f"[lyric-daemon] Found player: {self.player_service}")
        
        # We must explicitly tell the DBus daemon to route PropertiesChanged and Seeked signals to us
        await self.bus.call(
            Message(
                destination="org.freedesktop.DBus",
                path="/org/freedesktop/DBus",
                interface="org.freedesktop.DBus",
                member="AddMatch",
                signature="s",
                body=["type='signal',interface='org.freedesktop.DBus.Properties'"],
            )
        )
        await self.bus.call(
            Message(
                destination="org.freedesktop.DBus",
                path="/org/freedesktop/DBus",
                interface="org.freedesktop.DBus",
                member="AddMatch",
                signature="s",
                body=["type='signal',interface='org.mpris.MediaPlayer2.Player',member='Seeked'"],
            )
        )
        
        self.bus.add_message_handler(self._on_message)

        try:
            props = await dbus_get_all_properties(
                self.bus, self.player_service, MPRIS_PATH, PLAYER_IFACE
            )
            metadata = props.get("Metadata")
            if metadata:
                await self._track_changed(metadata)
        except Exception as exc:
            print(f"[lyric-daemon] Could not read initial state: {exc}")

    def _on_message(self, msg: Message) -> bool:
        if msg.message_type == MessageType.SIGNAL and msg.sender is not None:
            if msg.member == "PropertiesChanged" and msg.interface == PROPERTIES_IFACE:
                iface_name = msg.body[0]
                if iface_name == PLAYER_IFACE:
                    changed = msg.body[1]
                    unwrapped = {}
                    for k, v in changed.items():
                        try:
                            unwrapped[k] = v.value
                        except AttributeError:
                            unwrapped[k] = v
                    asyncio.ensure_future(self._handle_props_changed(unwrapped))
            elif msg.member == "Seeked" and msg.interface == PLAYER_IFACE:
                asyncio.ensure_future(self._handle_seek())
        return False

    async def _handle_seek(self) -> None:
        print("[lyric-daemon] Seek detected. Resyncing timeline...")
        self.next_index = 0
        await self._sync_position()
        await self._schedule_next()

    async def _handle_props_changed(self, changed: dict) -> None:
        if "Metadata" in changed:
            await self._track_changed(changed["Metadata"])
        if "PlaybackStatus" in changed:
            status = changed["PlaybackStatus"]
            if status == "Paused":
                print("[lyric-daemon] Paused")
                self._cancel_timer()
            elif status == "Playing":
                print("[lyric-daemon] Playing")
                self.next_index = 0
                await self._sync_position()
                await self._schedule_next()

    # ------------------------------------------------------------------
    # Track handling
    # ------------------------------------------------------------------
    async def _track_changed(self, metadata: dict) -> None:
        def extract(key: str, default=""):
            v = metadata.get(key)
            if v is None: return default
            try: return v.value
            except AttributeError: return v

        artist = extract("xesam:artist", [])
        if isinstance(artist, list):
            artist = artist[0] if artist else ""
        title = extract("xesam:title", "")
        track_id = extract("mpris:trackid", "")

        if not hasattr(self, 'current_title'):
            self.current_title = None

        if track_id == self.current_track_id and title == self.current_title:
            return

        self.current_track_id = track_id
        self.current_title = title
        self._cancel_timer()

        # If there's an ongoing download, cancel it so we don't overwrite/confuse states
        if getattr(self, '_download_task', None) and not self._download_task.done():
            self._download_task.cancel()

        print(f"[lyric-daemon] Track: {artist} - {title}")

        self._download_task = asyncio.create_task(self._resolve_lyrics(artist, title))

    async def _resolve_lyrics(self, artist: str, title: str) -> None:
        """Locates lyrics locally or fetches from LRCLIB."""
        lrc_path = locate_lrc(artist, title)

        if not lrc_path and title:
            query = clean_query(title, artist)
            print(f"[lyric-daemon] Local .lrc missing. Searching LRCLIB for: '{query}'")

            synced_lyrics = await fetch_lrclib(query)
            if synced_lyrics:
                safe_title = title.replace('/', '_')
                safe_artist = artist.replace('/', '_')
                filename = f"{safe_artist} - {safe_title}.lrc" if safe_artist else f"{safe_title}.lrc"

                lrc_path = LYRIC_DIR / filename
                LYRIC_DIR.mkdir(parents=True, exist_ok=True)

                try:
                    lrc_path.write_text(synced_lyrics, encoding='utf-8')
                    print(f"[lyric-daemon] Successfully downloaded lyrics to {lrc_path}")
                except Exception as e:
                    print(f"[lyric-daemon] Failed to save downloaded lyrics: {e}", file=sys.stderr)
            else:
                print(f"[lyric-daemon] No synced lyrics found on LRCLIB for '{query}'")

        if lrc_path and lrc_path.is_file():
            try:
                self.lyrics = parse_lrc(lrc_path.read_text(encoding="utf-8"))
                print(f"[lyric-daemon] Loaded {len(self.lyrics)} lyric lines")
            except Exception as exc:
                print(f"[lyric-daemon] Parse error: {exc}", file=sys.stderr)
                self.lyrics = [(0, "Lyric parse error")]
        else:
            self.lyrics = [(0, "No synced lyrics available")]

        self.next_index = 0
        await self._sync_position()
        await self._schedule_next()

    async def _sync_position(self) -> None:
        try:
            pos_us = await dbus_get_property(
                self.bus, self.player_service, MPRIS_PATH,
                PLAYER_IFACE, "Position"
            )
            self.start_position_ms = int(pos_us // 1_000)
        except Exception:
            self.start_position_ms = 0
        self.start_monotonic = asyncio.get_event_loop().time()

    # ------------------------------------------------------------------
    # Timing & emission
    # ------------------------------------------------------------------
    def _cancel_timer(self) -> None:
        if self._next_timer is not None:
            self._next_timer.cancel()
            self._next_timer = None

    def _current_position_ms(self) -> int:
        elapsed = asyncio.get_event_loop().time() - self.start_monotonic
        return self.start_position_ms + int(elapsed * 1_000)

    async def _schedule_next(self) -> None:
        self._cancel_timer()

        if self.next_index >= len(self.lyrics):
            return

        ts, _ = self.lyrics[self.next_index]
        current_ms = self._current_position_ms()

        while self.next_index < len(self.lyrics) and self.lyrics[self.next_index][0] < current_ms:
            self.next_index += 1

        if self.next_index >= len(self.lyrics):
            return

        ts, _ = self.lyrics[self.next_index]
        delay = max(0.0, (ts - current_ms) / 1_000.0)

        loop = asyncio.get_event_loop()
        self._next_timer = loop.call_later(delay, self._fire_lyric)

    def _fire_lyric(self) -> None:
        self._next_timer = None
        asyncio.ensure_future(self._emit_current())

    async def _emit_current(self) -> None:
        if self.next_index >= len(self.lyrics):
            return

        ts, text = self.lyrics[self.next_index]

        if self.next_index + 1 < len(self.lyrics):
            duration = self.lyrics[self.next_index + 1][0] - ts
        else:
            duration = 5_000

        intensity = "high" if "!" in text else "medium"

        # If it's a fallback message, let's keep it visible longer so the user can read it
        if text == "No synced lyrics available":
            duration = 5000

        payload = {"text": text, "duration_ms": duration, "intensity": intensity}
        await self._send_payload(payload)

        self.next_index += 1
        await self._schedule_next()

    # ------------------------------------------------------------------
    # Unix-socket server
    # ------------------------------------------------------------------
    async def _start_socket_server(self) -> None:
        if self._socket_server is not None:
            return

        SOCKET_PATH.parent.mkdir(parents=True, exist_ok=True)
        if SOCKET_PATH.exists():
            SOCKET_PATH.unlink()

        async def _client_connected(
            reader: asyncio.StreamReader, writer: asyncio.StreamWriter
        ):
            if self._client_writer is not None:
                try:
                    self._client_writer.close()
                    await self._client_writer.wait_closed()
                except Exception:
                    pass
            self._client_writer = writer
            print("[lyric-daemon] Client connected to socket")
            try:
                await reader.read()
            finally:
                if self._client_writer is writer:
                    self._client_writer = None
                try:
                    writer.close()
                    await writer.wait_closed()
                except Exception:
                    pass
                print("[lyric-daemon] Client disconnected")

        try:
            self._socket_server = await asyncio.start_unix_server(
                _client_connected, path=str(SOCKET_PATH)
            )
            print(f"[lyric-daemon] Socket listening at {SOCKET_PATH}")
        except Exception as exc:
            print(f"[lyric-daemon] Socket setup failed: {exc}", file=sys.stderr)

    async def _send_payload(self, payload: dict) -> None:
        data = (json.dumps(payload) + "\n").encode("utf-8")

        if self._client_writer is not None:
            try:
                self._client_writer.write(data)
                await self._client_writer.drain()
                return
            except Exception as exc:
                print(f"[lyric-daemon] Write error: {exc}", file=sys.stderr)
                self._client_writer = None

        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()

    # ------------------------------------------------------------------
    # Main run loop
    # ------------------------------------------------------------------
    async def run(self) -> None:
        await self._start_socket_server()
        await self.init_bus()
        print("[lyric-daemon] Ready — waiting for tracks...")

        stop = asyncio.Event()
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop.set)
        await stop.wait()

    # ------------------------------------------------------------------
    # Graceful shutdown
    # ------------------------------------------------------------------
    async def close(self) -> None:
        self._cancel_timer()
        if self._download_task and not self._download_task.done():
            self._download_task.cancel()
        if self._client_writer:
            try:
                self._client_writer.close()
                await self._client_writer.wait_closed()
            except Exception:
                pass
        if self._socket_server:
            self._socket_server.close()
            await self._socket_server.wait_closed()
        if SOCKET_PATH.exists():
            try:
                SOCKET_PATH.unlink()
            except Exception:
                pass
        if self.bus:
            self.bus.disconnect()


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------


def main() -> None:
    daemon = LyricDaemon()

    async def _run():
        try:
            await daemon.run()
        finally:
            await daemon.close()

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        pass
    print("[lyric-daemon] Shut down.")


if __name__ == "__main__":
    main()
