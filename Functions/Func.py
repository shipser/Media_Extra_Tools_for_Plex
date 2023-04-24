#!/usr/bin/env python3

##########################################################
##########################################################
## Writen By: Shay Pasvolsky | Apr 21st, 2023           ##
## Last Update: Apr 22st, 2023                          ##
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
def Get_TV_Movie_Name(File_Path, FType, MPfx, SPfx, SLang):
    try:
        # Try To Get The TV Show Or Movie Name
        if (FType == "TV"):
            TVMovie_Name = re.split(
                r' -', (re.split(r'.S\d+E\d+', (re.split(r'/', File_Path)[-1]))[0]))[0]
        elif (FType == "Movie"):
            # Build The Delimiter To Check
            Deli = MPfx.upper() + "|" + MPfx.lower() + "|" + \
                SPfx.upper() + "|" + SPfx.lower() + "|" + SLang.lower() + "|" + SLang.upper()
            TVMovie_Name = re.split(Deli, re.split(r'/', File_Path)[-1])[0]
        else:
            TVMovie_Name = "No_Name"
        return TVMovie_Name
    except:
        # Return Error
        return "Not A TV Show Or Movie File!"
# os.path.filen


# Build New Path To Arrange The File
def Build_New_Name(File_Path, Season, Episode, ToM, NName, SLang, MPfx, SPfx):
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
def Val_New_Name(New_Name_User, Old_Name, New_Name_List):
    try:
        # Check if user supplied a new name, if yes, return it.
        if (New_Name_List != ""):
            return New_Name_List
        elif (New_Name_User != None):
            return New_Name_User
        else:  # Else return the extracted name
            return Old_Name
    except:
        # Return Failed If Failed To Run
        return Old_Name


# Move To New Location
def Rename_TV_Movie(Org_File, New_Name):
    try:
        # Build The New File Path
        New_Path = os.path.dirname(Org_File) + "/" + New_Name
        # Rename The File
        os.rename(Org_File, New_Path)
        return True
    except:
        return False


# Check If Path Has More Then One TV Show And / Or Movie
def Val_One_TV_Movie(Files_In_Dir, MPfx, SPfx, SLang):
    try:
        Count = 0  # Set blank counter
        # Detect If Movie
        if (Get_Season_Episode(Files_In_Dir[0])[0] == "Empty"):
            MoT = "Movie"
        else:  # Set To TV
            MoT = "TV"
        # Get The First TV Show Or Movie Name
        FName = Get_TV_Movie_Name(Files_In_Dir[0], MoT, MPfx, SPfx, SLang)
        for f in Files_In_Dir:
            # Detect If Movie
            if (Get_Season_Episode(f)[0] == "Empty"):
                MoT = "Movie"
            else:  # Set To TV
                MoT = "TV"
            # Get The First TV Show Or Movie Name
            F_Name = Get_TV_Movie_Name(f, MoT, MPfx, SPfx, SLang)
            # Check If Not Identical To First Name And Increment The Counter
            if (F_Name != FName):
                Count += 1
        if (Count):  # If More Then One Name Return False, Else Return True
            return False
        else:
            return True
    except:
        return False


# Load And Select A List
def Get_List(List_Path):
    try:
        if (os.path.isfile(List_Path)):  # Make sure the file exists
            with open(List_Path) as Lines:  # Read the file
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


# Move Files Into Correct Location
def Move_Media(File_To_Move, New_Location, ToM, SeasPfx, SeasNum):
    try:
        # Check if the Source Exists, if not, exit
        if (not os.path.isfile(File_To_Move)):
            return False
        # Add Season Folder to the new path
        if (ToM == "TV" and (New_Location.upper().find(SeasPfx.upper()) == int("-1"))):
            # If New Location Does Not Have / at the end,  add it
            if (not New_Location.endswith("/")):
                New_Location = New_Location + "/"
            # Add Season Folder Name
            New_Location = New_Location + SeasPfx + " " + SeasNum
        # Check if the target exists, if not create it
        if (not os.path.isdir(New_Location)):
            os.makedirs(New_Location)
        # Build The New Path With The Name Of The File
        if (New_Location.endswith("/")):
            New_Location = New_Location + re.split(r'/', File_To_Move)[-1]
        else:
            New_Location = New_Location + "/" + \
                re.split(r'/', File_To_Move)[-1]
        # Check If File Exists in destination and move if not
        if (not os.path.isfile(New_Location)):
            os.rename(File_To_Move, New_Location)
        else:  # Abort if alredy exists, and notify the user.
            print("File '{}' Already Exists in the new location, File move aborted!".format(
                re.split(r'/', File_To_Move)[-1]))
        return True
    except:
        return False


# Remove Empty Folders
def CleanUp_SRC(src, rmsrc=False):
    try:
        # Check Every Folder If Empty And Remove IT
        Files_In_Dir = [os.path.join(root, name) for root, dirs, files in os.walk(
            src) for name in files if name.lower()]  # Scan for files in the directory and subdirectorie(s)
        for f in Files_In_Dir:  # Itirate threw files
            # Check if it is a hidden file (starts with a .)
            if (re.split(r'/', f.lower())[-1].startswith(".")):
                os.remove(f)  # Remove the hidden file
                # remove the entery from the list to continue
                Files_In_Dir.remove(f)
        Dirs_In_Dir = [os.path.join(root, name) for root, dirs, files in os.walk(
            src) for name in dirs if name.lower()]  # Build a list of all subdirectories
        for d in Dirs_In_Dir:  # Itirate threw the sub directories
            if (Is_Dir_Empty(d)):  # Check if the subdirectory is empty
                os.rmdir(d)  # Remove the subdirectory
                # Remove the subdirectory Entry from the list
                Dirs_In_Dir.remove(d)
        if (not len(Dirs_In_Dir) and rmsrc and Is_Dir_Empty(src)):
            os.rmdir(src)
        return True
    except:
        return False


# Check If Dir Is Empty
def Is_Dir_Empty(src):
    with os.scandir(src) as scan:
        return next(scan, None) is None


# Organize The SRC Folder
def Org_TV_Movie(src, Msfx, Ssfx, Lsfx, Spfx, RenameSRC=False):
    try:
        # Make Sure The Path Is A Directory
        if (os.path.isdir(src)):
            FDir = Get_Files_In_Show_Folder(
                src, Msfx, Ssfx)  # Get the file list
            # Check If Path Contains Only On TV Show Or One Movie
            OneSM = Val_One_TV_Movie(FDir, Msfx, Ssfx, Lsfx)
            # Check if only one TV Show or Movie is Present In The Source Directory
            if (OneSM):
                # Detect if Movie Or TV Show
                # Get Season and Episode number for the first file
                Seas, Epi = Get_Season_Episode(FDir[0])
                # Check If There Is A Season And Decide If It Is A Movie Or TV
                if (Seas == "Empty"):  # Movie
                    MoT = "Movie"  # Set Media Type For Futere Use
                else:  # TV Show
                    MoT = "TV"  # Set Media Type For Futere Use
                # Extract TV Show Or Movie Name From The File
                TV_Movie_Name = Get_TV_Movie_Name(
                    FDir[0], MoT, Msfx, Ssfx, Lsfx)
                # Make Sure Tha Path Ends With /
                if (not src.endswith("/")):
                    src = src + "/"
                # Check If The Source Folder Is Uniqe To The TV Show Or Movie, If Not Add The TV Show Or Movie Name To The New Path
                if (src.lower().find(TV_Movie_Name.lower()) != int("-1")):
                    Uni = True
                    dst = src
                else:
                    Uni = False
                    dst = src + TV_Movie_Name + "/"
                # Loop threw all the files int the folder
                for f in FDir:
                    # Get Season and Episode number for the first file
                    Seas, Epi = Get_Season_Episode(re.split(r'/', f)[-1])
                    # Move The File To New Location
                    Move_Media(f, dst, MoT, Spfx, Seas)
                    # Clean Old Empty Folders
                    CleanUp_SRC(src)
                # Rename The Source Folder If The User Asked For It
                # if (RenameSRC):
                #os.rename(src, "")
                return True
            else:
                print("Multi Show / Movie Source!")
                return False
        else:
            print("Source provided is not a directory!")
            return False
    except:
        print("Failed to organize the source folder!!")
        return False
