import re

with open('dots/.config/quickshell/ii/modules/common/Appearance.qml', 'r') as f:
    content = f.read()

# Add colMagic, colMagicHover, colMagicActive, colMagicContainer, etc
magic_tokens = """        // Magic (Ralsei OS)
        property color colMagic: ColorUtils.mix(m3colors.m3primary, "#5fe28d", 0.6) // Blend primary with a soft Ralsei green
        property color colMagicHover: ColorUtils.mix(colMagic, colOnMagic, 0.2)
        property color colMagicActive: ColorUtils.mix(colMagic, colOnMagic, 0.4)
        property color colOnMagic: m3colors.m3onPrimary
        property color colMagicContainer: ColorUtils.mix(m3colors.m3primaryContainer, "#1a3b2a", 0.5) // Dark magical surface
        property color colOnMagicContainer: ColorUtils.mix(m3colors.m3onPrimaryContainer, "#5fe28d", 0.3)
"""

# Insert just before // Misc
content = content.replace('        // Misc', magic_tokens + '        // Misc')

# Tweak layer 0 to have a slight dark world tint if darkmode
dark_world_tweak = """        property color colLayer0Base: ColorUtils.mix(m3colors.m3background, m3colors.m3primary, Config.options.appearance.extraBackgroundTint ? 0.99 : 1)"""
dark_world_tweak_new = """        property color colLayer0Base: root.m3colors.darkmode ? 
            ColorUtils.mix(m3colors.m3background, "#0c1512", 0.15) : // Slight Dark World tint for Ralsei OS
            ColorUtils.mix(m3colors.m3background, m3colors.m3primary, Config.options.appearance.extraBackgroundTint ? 0.99 : 1)"""
content = content.replace(dark_world_tweak, dark_world_tweak_new)

with open('dots/.config/quickshell/ii/modules/common/Appearance.qml', 'w') as f:
    f.write(content)

