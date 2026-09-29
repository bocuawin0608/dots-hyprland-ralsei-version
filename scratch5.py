import re

with open('dots/.config/quickshell/ii/modules/ii/sidebarLeft/aiChat/AiMessage.qml', 'r') as f:
    content = f.read()

# Make AI bubbles have magical styling
old_bg_color = "color: Appearance.colors.colLayer1"
new_bg_color = """color: (messageData?.role == 'assistant') ? ColorUtils.transparentize(Appearance.colors.colMagicContainer, 0.4) : Appearance.colors.colLayer1
    border.color: (messageData?.role == 'assistant') ? ColorUtils.transparentize(Appearance.colors.colMagic, 0.2) : "transparent"
    border.width: (messageData?.role == 'assistant') ? 1 : 0"""
content = content.replace(old_bg_color, new_bg_color)

# Make the header for AI messages have a strong magic color
old_header_color = "color: Appearance.colors.colSecondaryContainer"
new_header_color = "color: (messageData?.role == 'assistant') ? ColorUtils.transparentize(Appearance.colors.colMagicContainer, 0.2) : Appearance.colors.colLayer1Hover"
content = content.replace(old_header_color, new_header_color)

with open('dots/.config/quickshell/ii/modules/ii/sidebarLeft/aiChat/AiMessage.qml', 'w') as f:
    f.write(content)

