with open('dots/.config/hypr/hyprland/keybinds.lua', 'r') as f:
    content = f.read()

# Add Ctrl+Shift+Y keybind for subtitle mode
keybind = """hl.bind("CTRL + SHIFT + Y", hl.dsp.exec_cmd("quickshell -c 'qs.services.Ipc.send(\\"subtitle\\", \\"toggle\\")'"), { description = "Toggle Ralsei Subtitle Mode" })
"""

if "CTRL + SHIFT + Y" not in content:
    content = content + "\\n" + keybind

with open('dots/.config/hypr/hyprland/keybinds.lua', 'w') as f:
    f.write(content)

