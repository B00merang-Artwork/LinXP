# LinXP
Rebirth of Windows XP icon theme for linux (currently in development)

# Compilation

Requires python 3 and the python-yaml library

## Simple usage

Navigate to icon-build and run `./compile_icon_theme.py`. This will make a new
directory called "icon_theme" in the same folder with the cursor and UI icon
themes

## Advanced usage...good for testing

Navigate to icon-build and run `rm -rf ~/.icons/LinXP_testing/ && ./compile_icon_theme.py -o ~/.icons/LinXP_testing`

This will make a working icon theme (LinXP_testing) in the user's home directory
and simultaneously nuke the old version if it exists (effectively an overwrite).

Run this after any changes are made to rapidly test.
