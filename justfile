JUST:="just --justfile="+justfile()

@_all:
    {{ JUST }} --list

debug:
    nvim --cmd "set rtp+={{ justfile_directory() }}" -u none

python-profile FILENAME:
    python scripts/python-profile.py total_calls {{ FILENAME }} 
