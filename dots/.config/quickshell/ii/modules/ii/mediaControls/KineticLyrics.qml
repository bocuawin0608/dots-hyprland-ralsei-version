import QtQuick
import QtQuick.Effects
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import Quickshell.Hyprland
import qs.modules.common

PanelWindow {
    id: root
    
    // Ghost overlay properties: Overlay layer, no keyboard focus, click-through mask
    WlrLayershell.namespace: "quickshell:lyrics"
    WlrLayershell.layer: WlrLayer.Overlay
    WlrLayershell.keyboardFocus: WlrKeyboardFocus.None
    exclusionMode: ExclusionMode.Ignore
    color: "transparent"
    
    // Completely transparent to mouse clicks (click-through)
    mask: Region {
        item: null
    }

    anchors {
        top: true
        bottom: true
        left: true
        right: true
    }

    property bool isOpen: false

    IpcHandler {
        target: "lyrics"
        function toggle() {
            root.isOpen = !root.isOpen;
        }
    }

    GlobalShortcut {
        name: "lyricsToggle"
        description: "Toggles full-screen Kinetic Lyrics"
        onPressed: root.isOpen = !root.isOpen
    }

    // Trigger an animated notification when toggled
    onIsOpenChanged: {
        spawnLyric({
            text: isOpen ? "LYRICS ON" : "LYRICS OFF",
            duration_ms: 1500,
            intensity: "high"
        })
    }

    // Container for spawned lyrics that obeys isOpen toggle
    Item {
        id: lyricsContainer
        anchors.fill: parent
        opacity: root.isOpen ? 1 : 0
        visible: opacity > 0
        Behavior on opacity {
            NumberAnimation { duration: 250 }
        }
    }

    // Continuous Unbuffered Socket Reader
    Process {
        id: socketProc
        running: true
        // FORCE unbuffered output from netcat
        command: ["bash", "-c", "stdbuf -oL nc -U ~/.config/quickshell/ii/lyrics_socket"]
        stdout: SplitParser {
            onRead: data => {
                console.log("[KineticLyrics] RAW: " + data);
                if (data.trim().length === 0) return;
                try {
                    let payloads = data.trim().split('\n');
                    for (let raw of payloads) {
                        if (raw.trim().length === 0) continue;
                        let payload = JSON.parse(raw);
                        spawnLyric(payload);
                    }
                } catch(e) {
                    console.log("[KineticLyrics] Failed to parse lyric JSON: ", e);
                }
            }
        }
        onExited: reconnectTimer.start()
    }

    Timer {
        id: reconnectTimer
        interval: 1000
        onTriggered: socketProc.running = true
    }

    Component {
        id: lyricComponent
        Item {
            id: lyricItem
            anchors.fill: parent

            property string text: ""
            property int durationMs: 1000
            property string intensity: "high"

            Text {
                id: lyricText
                anchors.centerIn: parent
                text: lyricItem.text
                color: Appearance.colors.ralseiCream
                font.family: Appearance.font.family.title
                font.pixelSize: lyricItem.intensity === "high" ? Appearance.font.pixelSize.title * 3.5 : Appearance.font.pixelSize.title * 2.5
                font.weight: lyricItem.intensity === "high" ? Font.Black : Font.Bold
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.WordWrap
                width: parent.width * 0.9

                style: Text.Outline
                styleColor: Appearance.colors.ralseiBackground
            }
            
            MultiEffect {
                source: lyricText
                anchors.fill: lyricText
                autoPaddingEnabled: true
                blurEnabled: true
                blurMax: 30
                blur: 1.0
                shadowEnabled: true
                shadowColor: Appearance.colors.ralseiMagic
                shadowBlur: 2.0
                shadowOpacity: lyricItem.intensity === "high" ? 0.9 : 0.6
                z: -1
            }

            scale: 1.5
            opacity: 0.0

            ParallelAnimation {
                id: inAnim
                running: true
                NumberAnimation {
                    target: lyricItem
                    property: "scale"
                    to: 1.0
                    duration: 350
                    easing.type: Easing.OutBack
                    easing.overshoot: 1.5
                }
                NumberAnimation {
                    target: lyricItem
                    property: "opacity"
                    to: 1.0
                    duration: 250
                    easing.type: Easing.OutCubic
                }
                onFinished: outTimer.start()
            }

            Timer {
                id: outTimer
                interval: Math.max(0, lyricItem.durationMs - 350)
                onTriggered: outAnim.start()
            }

            ParallelAnimation {
                id: outAnim
                NumberAnimation {
                    target: lyricItem
                    property: "scale"
                    to: 1.2
                    duration: 250
                    easing.type: Easing.InBack
                }
                NumberAnimation {
                    target: lyricItem
                    property: "opacity"
                    to: 0.0
                    duration: 250
                    easing.type: Easing.InCubic
                }
                // CRITICAL: Garbage collect the memory
                onFinished: lyricItem.destroy()
            }
        }
    }

    function spawnLyric(payload) {
        if (!payload.text) return;
        lyricComponent.createObject(lyricsContainer, {
            "text": payload.text,
            "durationMs": payload.duration_ms || 2000,
            "intensity": payload.intensity || "high"
        });
        console.log("[KineticLyrics] SPAWNED: " + payload.text);
    }
}
