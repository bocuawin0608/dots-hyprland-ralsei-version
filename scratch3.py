import re

with open('dots/.config/quickshell/ii/modules/ii/overview/OverviewWindow.qml', 'r') as f:
    content = f.read()

# Replace the color handling with the Magic Layer
color_section = """            color: pressed ? ColorUtils.transparentize(Appearance.colors.colLayer2Active, 0.5) : 
                hovered ? ColorUtils.transparentize(Appearance.colors.colLayer2Hover, 0.7) : 
                ColorUtils.transparentize(Appearance.colors.colLayer2)
            border.color : ColorUtils.transparentize(Appearance.m3colors.m3outline, 0.88)"""

new_color_section = """            color: pressed ? ColorUtils.transparentize(Appearance.colors.colMagicActive, 0.3) : 
                hovered ? ColorUtils.transparentize(Appearance.colors.colMagicHover, 0.5) : 
                ColorUtils.transparentize(Appearance.colors.colLayer2, 0.7)
            border.color : (hovered || pressed) ? Appearance.colors.colMagic : ColorUtils.transparentize(Appearance.colors.colMagicContainer, 0.5)"""

content = content.replace(color_section, new_color_section)

with open('dots/.config/quickshell/ii/modules/ii/overview/OverviewWindow.qml', 'w') as f:
    f.write(content)

