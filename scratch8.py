import re

with open('dots/.config/quickshell/ii/GlobalStates.qml', 'r') as f:
    content = f.read()

if "property bool subtitleModeOpen" not in content:
    content = content.replace('property bool sidebarRightOpen', 'property bool subtitleModeOpen: false\\n    property bool sidebarRightOpen')

with open('dots/.config/quickshell/ii/GlobalStates.qml', 'w') as f:
    f.write(content)

