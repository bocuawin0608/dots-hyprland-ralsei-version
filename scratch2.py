import re

with open('dots/.config/quickshell/ii/modules/ii/bar/BarContent.qml', 'r') as f:
    content = f.read()

# Make the bar background have a subtle border or glow based on the Ralsei Dark World aesthetic
content = content.replace('border.color: Appearance.colors.colLayer0Border', 'border.color: Appearance.colors.colMagicContainer')
content = content.replace('color: Config.options.bar.showBackground ? Appearance.colors.colLayer0 : "transparent"', 'color: Config.options.bar.showBackground ? Appearance.colors.colLayer0 : "transparent"')

with open('dots/.config/quickshell/ii/modules/ii/bar/BarContent.qml', 'w') as f:
    f.write(content)

