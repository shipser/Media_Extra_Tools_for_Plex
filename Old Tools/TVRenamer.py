#!/usr/bin/env python3

##########################################################
##########################################################
## Writen By: Shay Pasvolsky | Apr 12th, 2023           ##
## Last Update: Apr 14th, 2023                          ##
## Email: spasvolski@gmail.com                          ##
## GitHub: https://github.com/shipser                   ##
## Gitlab: @shipser                                     ##
## Licensce: GNU GPLv3                                  ##
## Version: 1.5.5-5                                     ##
## TO DO:                                               ##
##          [X] Allow for Dynamic shows based on        ##
##              input.                                  ##
##          [X] Add ability to rename Master folder     ##
##              name.                                   ##
##          [X] Add the abilty to reorginize folder     ##
##              structure of the show.                  ##
##          [X] Allow For Single or Multy Episode       ##
##               Without Season Folder.                 ##
##          [X] Add Support For Reorginazing Season     ##
##              Folders When Their Names Are Incorrect. ##
##          [X] Add TV Show List Folder names To Chose  ##
##              From To Use In The Programe With        ##
##              External File.                          ##
##          [X] Add A Function To Move The Episode      ##
##              Or Show Files To The Correct Location,  ##
##              Based On The TV Show List Or User       ##
##               Setting.                               ##
##          [ ] Add Ability To Add A New TV Show To     ##
##              The External List.                      ##
##          [ ] Add Funcuionality To Edit The External  ##
##              TV Show List.                           ##
##          [ ] Build Functionality For VIM Like Search ##
##              And Chose For The TV Show.              ##
##          [ ] Add Support For 'Shorts', 'Specials'    ##
##               And 'Extras' Folders.                  ##
##          [ ] Add The Ability To Reorganize A         ##
##              Multi-TV-Show Folder.                   ##
## Known Bugs:                                          ##
##              [X] Running TVRenamer.py with "src -ol  ##
##                  list" Tryes And Fails To Move The   ##
##                  Episode Files To The TV Show Folder.##
##                  Fix: Use The -m Flag At The End Of  ##
##                       The Command.                   ##
##                  Update: Using -oml have the same    ##
##                  Effect.                             ##
##                  Status: Fixed For All Variants,     ##
##                  Except: -oml, Errors On             ##
##                  "TVRenamer.py: error: unrecognized  ##
##                  arguments: listpath"                ##
##              [ ] Running TVRenamer.py with "src -o"  ##
##                  When The Show Has A folder Without  ##
##                  Season Number Will Name Folder And  ##
##                  The Files In That Folder            ##
##                  Incorrectly.                        ##
##                  Fix: No Fix                         ##
##              [ ] Running TVRenamer.py when files     ##
##                  Doesn't Have Season Or Episode      ##
##                  Numbers Will Fail.                  ##
##                  Fix: No Fix                         ##
##########################################################
##########################################################

###########
# Imports #
###########

import glob         # For the gathering of the files
import os           # Used to build the directory list, rename function
import re           # For Regex Strings
import argparse     # For the arguments
import shutil       # For folder deletion

###############################
# Global Variables Defenition #
###############################

#################
# User Settings #
#################

Show_Dir = ""       # Set the show directory path
Show_Name = ""      # Set The Name For The Show
Dest = None         # Set the new location to save the TV show

###########################
# Do Not Change From Here #
###########################

Show_Season_Dirs = []               # Seasons List
Files_In_Dir = []                   # File List
File_Sufix_Movies = ".mkv"          # Movie File Suffix
File_Sufix_Subtitles = ".srt"       # Movie File Suffix
Lang_File_Sufix = ".heb"            # Language Suffix For The Subtitles
Season_Folder_Prefix = "Season"     # Season folder prefix before the season number

############################
# Argument Parser Settings #
############################

parser = argparse.ArgumentParser(description="******************************************************************************************\n  TV Show file renamer by Shay Pasvolsky (C).\n\n  The program acceptes only srt and mkv files!\n\n\n  Notice:\n         1) -O And -S Cann't be used together!!\n         2) -L will overwrite -N and -M configuration!!\n         3) Do not try to combine -M -L to -ML!!\n  Cation: Move option works only on complete TV Show (withoit -O and -L), Single season (with or without -O and -L) or Single episode (with or without -O and -L)!!\n  Cation 2: No support for non seasonal folder - may result in unorganized show!!\n******************************************************************************************",
                                 usage='%(prog)s [OPTIONS]', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("Show", help="Source directory of the show")
parser.add_argument('-N', '-n', '--NewSName', help="New Name for the show")
parser.add_argument('-O', '-o', '--Organaize', action='store_true',
                    help="Organize the show - add a sub dir for Season (with number) and move the files inside, then rename based on the formating. make sure there are no subfolders inside!!")
parser.add_argument('-R', '-r', '--ReName', action='store_true',
                    help="Rename the main show folder.")
parser.add_argument('-S', '-s', '--SeasonRename', action='store_true',
                    help="Rename the season folder\s.")
parser.add_argument('-M', '-m', '--Move',
                    help="Move the TV Show Episodes to the path provided.", nargs='?', default="Empty")
parser.add_argument('-L', '-l', '--LoadList',
                    help="Load external TV show list and select the correct one.",)
args = parser.parse_args()

#######################
# Function Defenition #
#######################


# Get All Show Files, Returns a tuaple of file list array and number of seasons found
def Get_Files_In_Show_Folder(Show_Path):
    try:
        Show_Files = []  # Declare blank show file array
        Show_Season_Dirs = [
            f.path for f in os.scandir(Show_Path) if f.is_dir()]    # Get The Season Folders
        Seasons = len(Show_Season_Dirs)  # Save the nuber of seasons found
        if Seasons > 0:  # Check to see ther are season folders
            # Loop threw the Seasons
            for i in Show_Season_Dirs:
                # Get Video Files
                Show_Files += [f for f in glob.glob(
                    glob.escape(i) + "/*" + File_Sufix_Movies)]
                # Get Subtitle Files
                Show_Files += [f for f in glob.glob(
                    glob.escape(i) + "/*" + File_Sufix_Subtitles)]
            # Check if found any files or set to no files found messege
            Show_Files = ["No Files Found!"] if (
                len(Show_Files) < 1) else Show_Files
        else:
            Show_Files = ["No Files Found!"]
    except:
        Show_Files = ["No Files Found!"]
    return Show_Files, Seasons


# Extract Season and Episode Numbers, return tuaple
def Get_Season_Episode(File_Path):
    try:
        # Search for season number
        Seas = re.search(r'S\d+', File_Path.upper()).group()
        try:  # Search for episode number(s)
            # Try yo see if it is a multi episode file with a dash
            Epi = re.search(r'E\d+-E\d+', File_Path.upper()).group()
        except:
            try:
                # Try yo see if it is a multi episode file without a dash
                Epi = re.search(r'E\d+E\d+', File_Path.upper()).group()
            except:
                # Handle single episode file
                Epi = re.search(r'E\d+', File_Path.upper()).group()
    except:
        Seas = "Not Found!"
        Epi = "Not Found!"
    return Seas, Epi


# Test to check if it is an mkv,srt or other file
def det_MKV_SRT(File_Path):
    try:  # Check if MKV file
        MSO = re.search(r'MKV', File_Path.upper()).group()
    except:
        try:  # Check if SRT file
            MSO = re.search(r'SRT', File_Path.upper()).group()
        except:  # Set to other file type (will never get here)
            MSO = "Other"
    return MSO


# Rename the file
def Show_File_Rename(File_Path, ShowName):
    try:
        # Get the full path without the file name
        File_Dir = os.path.dirname(File_Path)
        # Build the new name string
        NewShowFile = Build_New_Name(File_Dir, ShowName, Get_Season_Episode(File_Path)[
            0], Get_Season_Episode(File_Path)[1], det_MKV_SRT(File_Path))
        try:  # Try to rename
            if (NewShowFile != ""):
                os.rename(File_Path, NewShowFile)
            resul = "OK"
        except:
            resul = "Failed"
    except:
        resul = "NOK"
    return resul


# Build New Name for the file: FDir = File Directory path, ShowName = The String for the show name, SeasonStr = Season string for the file, EpisodeStr = Episode string, ShowFileType = MKV or SRT
def Build_New_Name(FDir, ShowName, SeasonStr, EpisodeSTR, ShowFileType):
    try:
        TempEpisodeSTR = []
        # Check formating of multi epiisode file to match ExxExx in order to add - between episode numbers
        if (re.search(r'E\d+E\d+', EpisodeSTR.upper())):
            # Split the string to max of 3 parts
            TempEpisodeSTR = re.split(
                r'E', EpisodeSTR.upper(), maxsplit=2)
            # Build the new episode string, , ignore the firs blank and use the other two parts
            EpisodeSTR = "E" + TempEpisodeSTR[1] + "-E" + TempEpisodeSTR[2]
        NewFName = FDir + "/" + ShowName + " - " + SeasonStr + \
            EpisodeSTR  # Build the new file name without the extantion
        # Add the correct extantion
        NewFName = (NewFName + ".mkv") if (ShowFileType ==
                                           "MKV") else (NewFName + Lang_File_Sufix + ".srt")
    except:
        NewFName = ""
    return NewFName


# Organaize the structure of the tv show folder
def Folder_Org(Show_Path):
    try:
        Season = 0
        Show_Files = []
        Show_Season_Dirs = [f.path for f in os.scandir(
            Show_Path) if f.is_dir()]    # Get The Season Folders
        if (len(Show_Season_Dirs) == 0):
            # Get Video Files
            Show_Files += [f for f in glob.glob(
                glob.escape(Show_Path) + "/*" + File_Sufix_Movies)]
            # Get Subtitle Files
            Show_Files += [f for f in glob.glob(
                glob.escape(Show_Path) + "/*" + File_Sufix_Subtitles)]
            # Get Season number and create the folder "Season %d"
            if (len(Show_Files)):
                Season = re.split(
                    r'S', Get_Season_Episode(Show_Files[0])[0].upper(), maxsplit=1)[1]  # Get the season number from the first file found and strip the trailing s
                NewSeasonFolder = Show_Path + "/" + Season_Folder_Prefix + \
                    " " + Season  # Build the new path to create
                try:
                    os.mkdir(NewSeasonFolder)  # Create the new folder
                    for file in Show_Files:  # Loop threw the files
                        # Split the path to its elements
                        fileparts = re.split(r'/', file)
                        fileparts.insert(-1,
                                         Season_Folder_Prefix + " " + Season)  # Insert the newly created folder name to the list
                        fileparts = '/'.join(fileparts)  # Re build the path
                        # Move the files to the new folder
                        os.rename(file, fileparts)
                except:
                    print("Failed to create folder and move the files!")
                    return False
        return True
    except:
        print("Organaize Function Failed")
        return False


# Rename the season folders
def Season_Rename(Show_Path):
    try:
        Show_Season_Dirs = [f.path for f in os.scandir(
            Show_Path) if f.is_dir()]    # Get The Season Folders
        if (len(Show_Season_Dirs) != 0):
            for f in Show_Season_Dirs:
                # Split the path to it's elements
                fileparts = re.split(r'/', f)
                # Replace the folder name with the new name
                fileparts[-1] = Season_Folder_Prefix + " " + re.split(r'S', re.search(
                    r'S\d+', fileparts[-1]).group().upper())[-1]  # Build the new name for the folder
                fileparts = '/'.join(fileparts)  # Rebuild the path
                os.rename(f, fileparts)  # Rename the folder
        return True
    except:
        print("Season renaming failed!")
        return False


# Move TV Show Function
def Move_TV_Show(Show_Path, New_Show_Path, Files_In_Dir):
    try:
        if (os.path.isdir(Show_Path)):  # Make Sure Source exists.
            # Check if destination folder exists, if it exists then it is not a new TV show, handle with care.
            if (os.path.isdir(New_Show_Path)):
                # TO DO: Handle folder already there. two scanarios: one episode - check if season folder exists, create if not, and move the episode; multi episodes
                print("Destination folder exists.")
                # Make sure there are files to handle
                if (Files_In_Dir[0] != 'No Files Found!'):
                    # Build the Season folder string
                    Season_Folder = Season_Folder_Prefix + " " + \
                        re.split(r'S', Get_Season_Episode(
                            Files_In_Dir[0])[0])[1]
                    # Check If Season folder exists and move files into it.
                    if (os.path.isdir(New_Show_Path + "/" + Season_Folder)):
                        print("Moveing episode(s) to the new location!")
                        try:
                            for f in Files_In_Dir:  # Go threw all the files
                                # Check if the file already exists, if not continue
                                if not os.path.isfile(New_Show_Path + "/" + Season_Folder + "/" + re.split(r'/', f)[-1]):
                                    os.rename(
                                        f, New_Show_Path + "/" + Season_Folder + "/" + re.split(r'/', f)[-1])  # Move the file to the new location if
                                else:
                                    # delete the file if already exists in the new location
                                    os.remove(f)
                            # Remove the old directory
                            try:
                                shutil.rmtree(
                                    Show_Path, ignore_errors=False, onerror=None)
                                return True
                            except:
                                print("Failed to delete folder!")
                                return False
                            return True
                        except:
                            print("Failed to move the episodes!")
                            return False
                    else:  # If Season foldr does not exists create it and move files into it.
                        print(
                            "Season folder does not exists, creating it and moveing the episodes into it.")
                        try:
                            # Create the season folder
                            os.makedirs(New_Show_Path + "/" + Season_Folder)
                            # Move all th files
                            for f in Files_In_Dir:
                                os.rename(
                                    f, New_Show_Path + "/" + Season_Folder + "/" + re.split(r'/', f)[-1])
                            # Remove the old directory
                            try:
                                shutil.rmtree(
                                    Show_Path, ignore_errors=False, onerror=None)
                                return True
                            except:
                                print("Failed to delete folder!")
                                return False
                        except:
                            print("Failed to create the season folder!")
                            return False
                else:  # No files - Print an Error
                    print("No Files To Move!")
                    return False
            else:  # Handle the no destination folder scanario - new TV Show.
                # Tell the user the destinaion does not exists.
                print("Destination folder does not exists. Creating and moveing.")
                try:
                    # Create the destination folder (with full structure)
                    os.makedirs(New_Show_Path)
                    # Try to move the show folder to the new location.
                    os.rename(Show_Path, New_Show_Path)
                    return True
                except:
                    # Tell the user the move has failed.
                    print("Failed to move the TV Show to the new folder!")
                    return False
        else:
            # Tell the user the source does not exists.
            print("Source folder does not exists!")
            return False
    except:
        print("Failed to move!")  # General fail of the proccess
        return False


# Check TV show path validity
def Show_Path_Validate(Path_To_Check, Show_Name):
    try:
        # Extract the last folder name
        Show_Folder = re.split(r"/", Path_To_Check)[-1]
        if (Show_Name == Show_Folder):  # Check if the shot name is already in the path, return true if show name is needed to be added to the path
            return False
        else:
            return True
    except:
        # Tell the user ther is an error in the path
        print("Path is not valid!")
        return False


# Get TV Show List
def Get_TV_List(List_Path):
    try:
        if (os.path.isfile(args.LoadList)):  # Make sure the file exists
            with open(args.LoadList) as Lines:  # Read the file
                # read the contets of the file and split into lines
                Show_List_Unsplit = Lines.read().splitlines()
            Show_List = []  # Set a blank array for the show list
            index = 1  # Number the lines, start with 1
            MessegeToShow = ""
            for L in Show_List_Unsplit:  # Loop threw the lines and split them to show name and conatining folder
                Show_List.append(re.split(r' : ', L))
                MessegeToShow = MessegeToShow + "\n" + str(index) + ") " + "Show name: " + re.split(r' : ', L)[
                    0] + ", location: " + re.split(r' : ', L)[1]  # Build the Meesege for the user to select a show
                index += 1
            # Add the question for the user to the messege
            MessegeToShow = MessegeToShow + "\n\nPlease Select a TV show number: "
            # Request a selection from the user.
            inp = input(MessegeToShow)
            # Return the TV show data array
            return Show_List[int(inp) - 1]
    except:
        print("Failed to load the list")
        return False

###################
# Start the Logic #
###################


def main():
    try:
        # Get The Show path to rename
        Show_Dir = args.Show
        # Get the new name for the Show, Check to see if blank, and set to the same as the source.
        if (args.NewSName == None):
            Show_Name = re.split(r'/', Show_Dir)[-1]
        else:  # If not blank, keep the new name
            Show_Name = args.NewSName
            if (args.ReName):  # Rename the master folder
                # Split the path to it's elements
                fileparts = re.split(r'/', Show_Dir)
                # Replace the folder name with the new name
                fileparts[-1] = Show_Name
                fileparts = '/'.join(fileparts)  # Rebuild the path
                os.rename(Show_Dir, fileparts)  # Rename the folder
                print("TV Show Folder Renamed Successfully!")
                Show_Dir = fileparts  # Set the folder path to work in to the new path
        Dest = None  # Clear the destination folder path before setting it
        # Load external TV show list and select one
        if (args.LoadList != None):
            # Get The Show list and selext one
            Selected_Show = Get_TV_List(args.LoadList)
            # Overwrite the manual user input for the TV Show name
            Show_Name = Selected_Show[0]
            # Save the location to move the show at the end
            Dest = Selected_Show[1]
        # Organaize the show folder
        if (args.Organaize):
            Folder_Org(Show_Dir)
            print("TV Show folder organaized successfully!")
        # Rename Season folders
        if (args.SeasonRename):
            Season_Rename(Show_Dir)
            print("Season folders renamed successfully!")
        # Get the list of files and number of seasons
        Files_In_Dir = Get_Files_In_Show_Folder(Show_Dir)
        # Loop threw the files and rename them
        for x in Files_In_Dir[0]:
            Show_File_Rename(x, Show_Name)
        print("TV Show files renamed with the correct structure!")
        # Move The Files To The Correct Location
        # Check if -m flag is used (it's value won't be "Empty"), if it does the go to the next step.
        if (args.Move != "Empty" or args.LoadList != None):
            # Get the updated list of files and number of seasons
            Files_In_Dir = Get_Files_In_Show_Folder(Show_Dir)
            # Check if list is lloaded
            if (Dest != None):
                # Move based on list location
                # Tell the user what is goning on
                print("Move to location based on external list!")
                # Build the path to move the show files
                New_Folder = Dest + "/" + Show_Name
                # Move the episodes
                Move_TV_Show(Show_Dir, New_Folder, Files_In_Dir[0])
            else:
                # Else check if user supplied a location to move to
                if (args.Move != None):
                    New_Folder = args.Move  # Start to build the new path to save
                    if (Show_Path_Validate(args.Move, Show_Name)):  # Add the Show name if needed
                        New_Folder += "/" + Show_Name
                    # Move the show to the new location
                    Move_TV_Show(Show_Dir, New_Folder, Files_In_Dir[0])
                    #print("Move to provided location: ", args.Move)
                else:
                    # No location supplied by the user or list
                    print("Destination location wasn't supplied, skipping the move!")
        print("Finished all the tasks successfully!!!")
    except:
        print("Run Failed")


if __name__ == "__main__":
    main()
