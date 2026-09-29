with open('dots/.config/quickshell/ii/panelFamilies/IllogicalImpulseFamily.qml', 'r') as f:
    content = f.read()

import_line = "import qs.modules.ii.subtitle"
if import_line not in content:
    content = content.replace("import qs.modules.ii.verticalBar", "import qs.modules.ii.verticalBar\\nimport qs.modules.ii.subtitle")

loader_line = "    PanelLoader { component: SubtitleOverlay {} }"
if loader_line not in content:
    content = content.replace("    PanelLoader { component: WallpaperSelector {} }", "    PanelLoader { component: WallpaperSelector {} }\\n" + loader_line)

with open('dots/.config/quickshell/ii/panelFamilies/IllogicalImpulseFamily.qml', 'w') as f:
    f.write(content)

