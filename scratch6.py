import re

for filename in ['anti-flashbang.glsl', 'anti-flashbang-weak.glsl']:
    path = f'dots/.config/quickshell/ii/services/hyprlandAntiFlashbangShader/{filename}'
    with open(path, 'r') as f:
        content = f.read()
    
    # Change vec3(0.0) to a dark magical green vec3(0.03, 0.06, 0.05)
    content = content.replace('vec3(0.0)', 'vec3(0.03, 0.05, 0.04)')
    
    with open(path, 'w') as f:
        f.write(content)

