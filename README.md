# Media_Extra_Tools_for_Plex

## **Extra tools to organeize media folders and files for Plex by Shay Pasvolsky**

Tools to organaize media librery for Plex, Kodi, Jellyfin and Emby.
*Test only with plex folder and file nameing scheme.*

- ***Current Version: v0.4.2-alpha***

### Features

1. **To Add**

## System Requirements (Based on tested systems, may work with different configurations)

### macOS

- Version: Monterey (12.6) and higher
- python version: 3.9.7 and higher

### Ubuntu

- Version: 20.04.6 and higher
- python version: 3.8.10 and higher

## How To Use

- Show Version: `./MET.py -v` `./MET.py -V` `./MET.py --Version`
- Get Help: `./Met.py -h` `./Met.py -H` `./Met.py --help`
- Organaize single TV episode, single movie, multiple TV episodes of the same show (same or different season), mixed TV and movie(s) folder: `./Met.py -s 'Path of the folder to work on' -o` `./Met.py -s 'Path of the folder to work on' -O` `./Met.py -s 'Path of the folder to work on' --Organaize`
- Rename a single TV show folder (one or more episoded, one or more seasons) or a single movie folder (single version only) to manual set name: `./Met.py -s 'Path of the folder to work on' -r -n "Name to set"` `./Met.py -s 'Path of the folder to work on' -R -N "Name to set"` `./Met.py -s 'Path of the folder to work on' --ReName --NewSName "Name to set"`
- Move a single TV show folder (one or more episoded, one or more seasons) or a single movie folder (single version only to manual set location without renaming: `./Met.py -s 'Path of the folder to work on' -m 'path for the location to move the files into'` `./Met.py -s 'Path of the folder to work on' -M 'path for the location to move the files into'` `./Met.py -s 'Path of the folder to work on' --Move 'path for the location to move the files into'`
- Move a single TV show folder (one or more episoded, one or more seasons) or a single movie folder (single version only to manual set location with renaming based on user manual set name: `./Met.py -s 'Path of the folder to work on' -m 'path for the location to move the files into' -n "Name to set"` `./Met.py -s 'Path of the folder to work on' -M 'path for the location to move the files into' -N "Name to set"` `./Met.py -s 'Path of the folder to work on' --Move 'path for the location to move the files into' --NewSName "Name to set`
- Rename based on external list: `./Met.py -s 'Path of the folder to work on' -r -n "Name to set" -l 'Path to the external media list'` `./Met.py -s 'Path of the folder to work on' -R -N "Name to set" -L 'Path to the external media list'` `./Met.py -s 'Path of the folder to work on' --ReName --NewSName "Name to set" --LoadList 'Path to the external media list'`
- Move and Rename based on external list:`./Met.py -s 'Path of the folder to work on' -m 'path for the location to move the files into' -l 'Path to the external media list'` `./Met.py -s 'Path of the folder to work on' -M 'path for the location to move the files into' -L 'Path to the external media list'` `./Met.py -s 'Path of the folder to work on' --Move 'path for the location to move the files into'  --LoadList 'Path to the external media list'`
- Remove original folder path if empty (only works after moveing the media): add `-c` or `-C` or `--CleanUp` after the Move command ==(before running the move command)==

### External TV and Movie List Format

**Every TV show or Movie has to be on a seperate line**
Line structure: `TV Show Name : Full path to the location to move to`
Example: `Andor {tvdb-393189} : /media/TV/`
