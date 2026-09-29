import re

with open('dots/.config/quickshell/ii/modules/common/models/AdaptedMaterialScheme.qml', 'r') as f:
    content = f.read()

magic_token = """    property color colMagic: ColorUtils.mix(root.colPrimary, "#5fe28d", 0.4)"""

content = content.replace('    property color colOnSecondaryContainer', magic_token + '\n    property color colOnSecondaryContainer')

with open('dots/.config/quickshell/ii/modules/common/models/AdaptedMaterialScheme.qml', 'w') as f:
    f.write(content)

