# Media Extra Tools for Plex

## **Extra tools to organeize media folders and files for Plex by Shay Pasvolsky**

Tools to organaize media librery for Plex, Kodi, Jellyfin and Emby.
*Tested only with plex folder and file nameing scheme.*

- ***Current Version: v0.4.4-alpha***

### Features

1. Organaize a folder containing one or more TV episodes or movies.
2. Rename single TV Show (one or more episodes) or Movie to user supplied name or from external list.
3. Move single TV Show (one or more episodes) or Movie to user supplied location or from external list.  
    a. Remove original folder after completeing a move.

## System Requirements (Based on tested systems, may work with different configurations)

### macOS

- Version: Monterey (12.6) and higher
- python version: 3.9.7 and higher

### Ubuntu

- Version: 20.04.6 and higher
- python version: 3.8.10 and higher

## How To Use?  
  
### MET.py

- Show Version:  
    `./MET.py -v`  
    `./MET.py -V`  
    `./MET.py --Version`  
    - Example: `./MET.py -v`  
    - Result: `MET (Media Extra Tools for plex) Version: v0.4.2-alpha`  
- Get Help:  
    `./Met.py -h`  
    `./Met.py -H`  
    `./Met.py --help`  
    - Example: `./MET.py -h`  
- Organaize single TV episode, single movie, multiple TV episodes of the same show (same or different season), mixed TV and movie(s) folder:  
    `./Met.py -s 'Path of the folder to work on' -o`  
    `./Met.py -s 'Path of the folder to work on' -O`  
    `./Met.py -s 'Path of the folder to work on' --Organaize`  
    - Example: `./Met.py -s '/media/' -o`  
- Rename a single TV show folder (one or more episoded, one or more seasons) or a single movie folder (single version only) to manual set name:  
    `./Met.py -s 'Path of the folder to work on' -r -n "Name to set"`  
    `./Met.py -s 'Path of the folder to work on' -R -N "Name to set"`  
    `./Met.py -s 'Path of the folder to work on' --ReName --NewSName "Name to set"`  
    - Example: `./Met.py -s '/media/TV/Andor' -r -n "Andor {tvdb-393189}"`  
- Move a single TV show folder (one or more episoded, one or more seasons) or a single movie folder (single version only to manual set location without renaming:  
    `./Met.py -s 'Path of the folder to work on' -m 'path for the location to move the files into'`  
    `./Met.py -s 'Path of the folder to work on' -M 'path for the location to move the files into'`  
    `./Met.py -s 'Path of the folder to work on' --Move 'path for the location to move the files into'`  
    - Example: `./Met.py -s '/media/TV/Andor' -m "/media/TV/Andor {tvdb-393189}"`  
- Move a single TV show folder (one or more episoded, one or more seasons) or a single movie folder (single version only to manual set location with renaming based on user manual set name:  
    `./Met.py -s 'Path of the folder to work on' -m 'path for the location to move the files into' -n "Name to set"`  
    `./Met.py -s 'Path of the folder to work on' -M 'path for the location to move the files into' -N "Name to set"`  
    `./Met.py -s 'Path of the folder to work on' --Move 'path for the location to move the files into' --NewSName "Name to set`  
    - Example: `./Met.py -s '/media/TV/Andor1' -m "/media/TV/" -n "Andor {tvdb-393189}"`  
- Rename based on external list:  
    `./Met.py -s 'Path of the folder to work on' -r -l 'Path to the external media list'`  
    `./Met.py -s 'Path of the folder to work on' -R -L 'Path to the external media list'`  
    `./Met.py -s 'Path of the folder to work on' --ReName --NewSName --LoadList 'Path to the external media list'`  
    - Example: `./Met.py -s '/media/TV/Andor' -r -l '/media/TV/MediaList.list'`  
- Move and Rename based on external list:  
    `./Met.py -s 'Path of the folder to work on' -m -l 'Path to the external media list'`  
    `./Met.py -s 'Path of the folder to work on' -M -L 'Path to the external media list'`  
    `./Met.py -s 'Path of the folder to work on' --Move --LoadList 'Path to the external media list'`  
    - Example: `./Met.py -s '/media/TV/Andor1' -m -l '/media/TV/MediaList.list'`  
- Remove original folder path if empty (only works after moveing the media):  
    add `-c` or `-C` or `--CleanUp` after the Move command ***(before running the move command)***  
    - Example: `./Met.py -s '/media/TV/Andor1' -m -l '/media/TV/MediaList.list' -c`  

### External TV and Movie List Format

Every TV show or Movie must be on a seperate line  

- Line structure:  
    - `TV Show Name : Full path to the location to move to`  
- Example:  
    - `Andor {tvdb-393189} : /media/TV/`  
