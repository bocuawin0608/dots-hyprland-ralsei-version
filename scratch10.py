import re

for filename in ['sdata/subcmd-install/3.files-legacy.sh', 'sdata/subcmd-install/3.files-exp.sh']:
    with open(filename, 'r') as f:
        content = f.read()

    # We can inject it around where XDG directories are ensured
    if "mkdir -p ~/Pictures/Wallpapers/Ralsei" not in content:
        content = content.replace('for i in "$XDG_BIN_HOME" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME"; do', 
                                  'v mkdir -p ~/Pictures/Wallpapers/Ralsei\\nfor i in "$XDG_BIN_HOME" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME"; do')

    with open(filename, 'w') as f:
        f.write(content)

