#!/usr/bin/env python3

##########################################################
##########################################################
## Writen By: Shay Pasvolsky | Apr 21st, 2023           ##
## Last Update: Apr 21st, 2023                          ##
## Email: spasvolski@gmail.com                          ##
## GitHub: https://github.com/shipser                   ##
## Gitlab: @shipser                                     ##
## Licensce: GNU GPLv3                                  ##
##########################################################
##########################################################

###########
# Imports #
###########

import os           # Used to build the directory list, rename function
import re           # For Regex Strings

#######################
# Function Defenition #
#######################


# Get all the movie and subtitle files in a path
def Get_Files_In_Show_Folder(Show_Path, MFileType, SubFileType):
    try:
        Show_Files = []  # Declare blank show file array
        # Get Files
        Show_Files = [os.path.join(root, name) for root, dirs, files in os.walk(
            Show_Path) for name in files if name.lower().endswith((MFileType, SubFileType))]
        # Make sure files were found, if not reset the list
        if (len(Show_Files) == 0):
            Show_Files = ["Empty"]
        # Return what was found
        return Show_Files
    except:
        # return an error
        return ["Error!!"]


# Extract Season and Episode Numbers
def Get_Season_Episode(File_Path):
    try:
        # Get Season Number Without The S
        Seas = re.split(
            r'S', (re.search(r'S\d+', File_Path.upper()).group()), maxsplit=2)[1]
        # Get Episode Number With The E's
        try:
            # Check for Ex-Ex format for multi-episode
            Epi = re.search(r'E\d+-E\d+', File_Path.upper()).group()
        except:
            try:
                # Check for ExEx format for multi-episode
                Epi = re.search(r'E\d+E\d+', File_Path.upper()).group()
            except:
                # Check for Ex format for single episode
                Epi = re.search(r'E\d+', File_Path.upper()).group()
        # Return Season and Episode Number
        return [Seas, Epi]
    except:
        # Return Unvalid Values
        return ["Empty", "Empty"]


# Extract TV Show Or Movie Name
def Get_TV_Movie_Name(File_Path, FType, MPfx, SPfx):
    try:
        # Try To Get The TV Show Or Movie Name
        if (FType == "TV"):
            TVMovie_Name = re.split(
                r' -', (re.split(r'.S\d+E\d+', (re.split(r'/', File_Path)[-1]))[0]))[0]
        elif (FType == "Movie"):
            # Build The Delimiter To Check
            Deli = MPfx.upper() + "|" + MPfx.lower() + "|" + \
                SPfx.upper() + "|" + SPfx.lower()
            TVMovie_Name = re.split(Deli, re.split(r'/', File_Path)[-1])[0]
        else:
            TVMovie_Name = "No_Name"
        return TVMovie_Name
    except:
        # Return Error
        return "Not A TV Show Or Movie File!"
# os.path.filen


# Build New Path To Arrange The File
def Build_New_Name(File_Path, Season, Episode, ToM, NName, SeasPFX, SLang, MPfx, SPfx):
    try:
        New_Path = os.path.dirname(File_Path) + "/"
        # Check if TV Or Movie Title
        if (ToM == "TV"):
            # Get Start Episode And End Episode
            Temp_Epi = re.split(r'E|-E', Episode.upper(), maxsplit=2)
            # Build The Episode Name
            New_Name = NName + " - S" + Season + "E" + Temp_Epi[1]
            # If the original file is a multi episode, adapt the new episode name
            if (len(Temp_Epi) > 2):
                New_Name += "-E" + Temp_Epi[2]
        elif (ToM == "Movie"):
            # Change The Movie Name To The New Name
            New_Name = NName
        else:
            # Error Out
            New_Name = "Error!!"
        # Check if MKV Or SRT file
        if (len(re.split(MPfx.upper(), File_Path.upper())) > 1):
            File_Type = "Mkv"
        else:
            File_Type = "Sub"
        if (New_Name != "Error!!"):
            if (File_Type == "Sub"):
                New_Name = New_Name + SLang + SPfx.lower()
            else:
                New_Name += MPfx.lower()
        New_Path += New_Name
        return New_Name, New_Path
    except:
        # Error Out
        return ["Error!!!", "Error!!!"]


# Validate New TV Or Movie Name
def Val_New_Name(New_Name, Old_Name):
    try:
        # Check if user supplied a new name, if yes, return it.
        if (New_Name != None):
            return New_Name
        else:  # Else return the extracted name
            return Old_Name
    except:
        # Return Failed If Failed To Run
        return Old_Name


# Move To New Location
def Rename_TV_Movie(Org_File, New_Name, MPfx):
    try:
        # if (Val_One_TV_Movie(Org_File, MPfx))
        # Build The New File Path
        New_Path = os.path.dirname(Org_File) + "/" + New_Name
        # Rename The File
        os.rename(Org_File, New_Path)
        return True
    except:
        return False


# Check If Path Has More Then One TV Show And / Or Movie
def Val_One_TV_Movie(Files_In_Dir, MPfx, SPfx):
    try:
        Count = 0  # Set blank counter
        # Detect If Movie
        if (Get_Season_Episode(Files_In_Dir[0])[0] == "Empty"):
            MoT = "Movie"
        else:  # Set To TV
            MoT = "TV"
        # Get The First TV Show Or Movie Name
        FName = Get_TV_Movie_Name(Files_In_Dir[0], MoT, MPfx, SPfx)
        for f in Files_In_Dir:
            # Detect If Movie
            if (Get_Season_Episode(f)[0] == "Empty"):
                MoT = "Movie"
            else:  # Set To TV
                MoT = "TV"
            # Get The First TV Show Or Movie Name
            F_Name = Get_TV_Movie_Name(f, MoT, MPfx, SPfx)
            # Check If Not Identical To First Name And Increment The Counter
            if (F_Name != FName):
                Count += 1
        if (Count):  # If More Then One Name Return False, Else Return True
            return False
        else:
            return True
    except:
        return False
