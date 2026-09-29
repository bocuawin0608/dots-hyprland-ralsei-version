with open('sdata/subcmd-install/3.files.sh', 'r') as f:
    content = f.read()

if "mkdir -p ~/Pictures/Wallpapers/Ralsei" not in content:
    content = content.replace('for i in "$XDG_BIN_HOME" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME"; do', 
                              'v mkdir -p ~/Pictures/Wallpapers/Ralsei\\nfor i in "$XDG_BIN_HOME" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME"; do')

with open('sdata/subcmd-install/3.files.sh', 'w') as f:
    f.write(content)
