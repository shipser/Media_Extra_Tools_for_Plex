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
import inquirer     # Used in LoadListSelector

#######################
# Function Defenition #
#######################


# Get all the movie and subtitle files in a path
def Get_Files_In_Show_Folder(Show_Path, MFileType, SubFileType):
    """
    Get all media file paths in the source folder.

    depends on:
        imports:
            os

    :param Show_Path: Media folder path to work on.
    :param MFileType: Media file suffix (like .mkv), must have dot at the start.
    :param SubFileType: Subtitle file suffix (like .srt), must have dot at the start.
    :return: [File path array] if found at least one file, ["Empty"] if no files found, ["Error!!"] on any error.
    """
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
    """
    Extract season number and episode number from a media file path.

    depends on:
        imports:
            re

    :param File_Path: Media file path to work on.
    :return: returns a tuaple of [Season number, Episode number] if extracted, on any error returns a tuaple of ["Empty", "Empty"]
    """
    try:
        # Make Sure To Use Only The File Name And Not The Full Path
        File_Path = re.split(r'/', File_Path)[-1]
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
    """
    Extract the Movie or TV Show Name from a path to a media file.

    depends on:
        imports:
            re

    :param File_Path: Media file path to work on.
    :param FType: Media type, must be "TV" or "Movie".
    :param MPfx: Media file suffix (like .mkv), must have dot at the start.
    :param SPfx: Subtitle file suffix (like .srt), must have dot at the start.
    :param SLang: Languge suffix for the subtitile name, mast have a dot at the start (like .heb).
    :return: returns the Name of the TV Show series or Movie extracted if succeded, if not, returns an error string.
    """
    try:
        # Try To Get The TV Show Or Movie Name
        if (FType == "TV"):
            TVMovie_Name = re.split(
                r' -', (re.split(r'.S\d+E\d+', (re.split(r'/', File_Path)[-1]), flags=re.IGNORECASE)[0]))[0]
        elif (FType == "Movie"):
            # Build The Delimiter To Check
            Deli = MPfx.upper() + "|" + MPfx.lower() + "|" + \
                SPfx.upper() + "|" + SPfx.lower() + "|" + SLang.lower() + "|" + SLang.upper()
            # Extract The TV Show Or Movie Name
            TVMovie_Name = re.split(Deli, re.split(
                r'/', File_Path)[-1], flags=re.IGNORECASE)[0]
        else:
            TVMovie_Name = "No_Name"
        return TVMovie_Name
    except:
        # Return Error
        return "Not A TV Show Or Movie File!"
# os.path.filen


# Build New Path To Arrange The File
def Build_New_Name(File_Path, Season, Episode, ToM, NName, SLang, MPfx, SPfx):
    """
    Build new file name and file path based on plex organization scheme.

    depends on:
        imports:
            os
            re

    :param File_Path: File path to work on..
    :param Season: Season number for TV Episode file.
    :param Episode: Episode number for TV Episode file.
    :param ToM: For TV Show File Set to "TV", For Movie file set to "Movie", everything else will give an error.
    :param NName: New TV Show or Movie Name.
    :param SLang: Languge suffix for the subtitile name, mast have a dot at the start (like .heb).
    :param MPfx: Media file suffix (like .mkv), must have dot at the start.
    :param SPfx: Subtitle file suffix (like .srt), must have dot at the start.
    :return: On any undefind error return an array of ["Error!!!", "Error!!!"], on ToM Error return an array of ["Error!!", invalid path], on success return an array of [New File Name, new file path]
    """
    try:
        # Get The Current File Directory
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
    """
    Check the new name is not enpty or None.

    depends on:
        Nothing

    :param New_Name_User: TV Show or Movie name supplied by user input.
    :param Old_Name: Original TV Show or Movie name.
    :param New_Name_List: TV Show or Movie name supplied by the user selection from the list.
    :return: The name from the list if available, if not then the user supplied name if available, else the original name.
    """
    try:
        # Check if user supplied a new name, if yes, return it.
        if (New_Name_List != "" and New_Name_List != None):
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
    """
    Rename a file.

    depends on:
        imports:
            os

    :param Org_File: File path to rename.
    :param New_Name: New name for the file.
    :return: True on success, False on any fail.
    """
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
    """
    Check if the path has only One TV Show or Movie in it (can be multiple files, jest have to belong to the same TV Show Or Movie).

    depends on:
        Functions:
            Get_Season_Episode
            Get_TV_Movie_Name

    :param Files_In_Dir: Two dimantional array of files.
    :param MPfx: Media file suffix (like .mkv), must have dot at the start.
    :param SPfx: Subtitle file suffix (like .srt), must have dot at the start.
    :param SLang: Languge suffix for the subtitile name, mast have a dot at the start (like .heb).
    :return: True if all the files belong to one TV Show or Movie, False on any fail or if not.
    """
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


# Move Files Into Correct Location
def Move_Media(File_To_Move, New_Location, ToM, SeasPfx, SeasNum):
    """
    Move Media file feo source to new location.

    depends on:
        imports:
            os
            re

    :param File_To_Move: File path to move.
    :param New_Location: Media folder to put the file in..
    :param ToM: if equals to "TV" treat as an TV episode file, else as a movie file.
    :param SeasPfx: Season folder prefix (like Season).
    :param SeasNum: season number for the TV Episode file.
    :return: True on success, False on any fail.
    """
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
    """
    Clean Up the source (src) folder by deleteing hidden files and removeing empty sub folders. if rmsrc is set to true, deletes the parent folder if empty.

    depends on:
        imports:
            os
            re
        Functions:
            Is_Dir_Empty

    :param src: path of folder to clean up.
    :return: True on success, False on fail.
    """
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
    """
    Make sure the folder provided is empty

    depends on:
        imports:
            os

    :param src: The path to check
    :return: True if empty.
    """
    with os.scandir(src) as scan:
        return next(scan, None) is None


# Organize The SRC Folder
def Org_TV_Movie(src, Msfx, Ssfx, Lsfx, Spfx):
    """
    Organize the path provided, put every TV Show  or Movie to the correct folder inside the original path.

    depends on:
        imports:
            os
            re
        Functions:
            Get_Files_In_Show_Folder
            Get_Season_Episode
            Get_TV_Movie_Name
            Move_Media
            CleanUp_SRC

    :param src: folder path to work on.
    :param Msfx: Media file suffix (like .mkv), must have dot at the start.
    :param Ssfx: Subtitle file suffix (like .srt), must have dot at the start.
    :param Lsfx: Languge suffix for the subtitile name, mast have a dot at the start (like .heb).
    :param Spfx: Season folder prefix (like Season).
    :return: True on success, False on any fail.
    """
    try:
        # Make Sure The Path Is A Directory
        if (os.path.isdir(src)):
            FDir = Get_Files_In_Show_Folder(
                src, Msfx, Ssfx)  # Get the file list
            # Loop threw all the files int the folder
            for f in FDir:
                # Get Season and Episode number for the first file
                Seas, Epi = Get_Season_Episode(re.split(r'/', f)[-1])
                # Check If There Is A Season And Decide If It Is A Movie Or TV
                if (Seas == "Empty"):  # Movie
                    MoT = "Movie"  # Set Media Type For Futere Use
                else:  # TV Show
                    MoT = "TV"  # Set Media Type For Futere Use
                # Extract TV Show Or Movie Name From The File
                TV_Movie_Name = Get_TV_Movie_Name(
                    f, MoT, Msfx, Ssfx, Lsfx)
                # Make Sure Tha Path Ends With /
                if (not src.endswith("/")):
                    src = src + "/"
                # Build The Destination Path
                # Check If The Source Folder Is Uniqe To The TV Show Or Movie, If Not Add The TV Show Or Movie Name To The New Path
                if (src.lower().find(TV_Movie_Name.lower()) != int("-1")):
                    dst = src
                else:
                    dst = src + TV_Movie_Name + "/"
                # Move The File To New Location
                Move_Media(f, dst, MoT, Spfx, Seas)
                # Clean Old Empty Folders
                CleanUp_SRC(src)
            # Return true if success.
            return True
        else:
            print("Source provided is not a directory!")
            return False
    except:
        print("Failed to organize the source folder!!")
        return False


# Check Source Directory Path Ends In / If Destination Is
def Check_SRC_DST(src, dst):
    """
    Check_SRC_DST checks src (source) and dst (destination) last charecter one againset each over and cheks if they both have /.
    If source deosn't have / while dst has - it adds / to the end of src.
    If src has but dst doesn't, it removes the / from src's end.
    examples:
    1. src = path/, dst = path/ -> result = src = path/
    2. src = path, dst = path -> result = src = path
    3. src = path, dst = path/ -> result = src + / = path/
    4. src = path/, dst = path -> result = src - / = path

    depends on:
        Nothing

    :param src: the source folder path.
    :param dst: the destination folder path.
    :return: The function returns fixed src after checking it.
    """
    try:
        # Set Starting point for non of the conditions met.
        src_t = src
        # Deal with / missing in src and not dst Or Vise Versa
        if (not src.endswith("/") and dst.endswith("/")):
            src_t = src + "/"  # Add / to src because dst has it and src doesn't
        elif (src.endswith("/") and not dst.endswith("/")):
            # Remove / from because dst doesn't have it and src has it
            src_t = src[:-1]
        return src_t
    except:
        # Return the origianl src if failed
        return src


# Build New Path
def Build_New_Path(src, TV_Movie_Name):
    """
    Function to build new folder path containing the show name (only once).

    depends on:
        imports:
            os

    :param src: the source folder path.
    :param TV_Movie_Name: the TV Show / Movie name.
    :return: returns new path with the TV Show / Movie name as the last folder, on any fail type, will return the original path.
    """
    try:
        # Make Sure The Path Is A Directory
        if (os.path.isdir(src)):
            # Make Sure src Has A Trailing /
            if (not src.endswith("/")):
                src = src + "/"
            # Make Sure The Media Name Provided
            if (TV_Movie_Name != ""):
                # Check To Make Sure That The Path doesn't have 'Media Name' named folder, and add it to the path
                if (src.lower().find(TV_Movie_Name.lower()) == int("-1")):
                    src_t = src + TV_Movie_Name + "/"
                else:
                    src_t = src
                return src_t
            else:
                print("No show name provided!")
                return src
        else:
            print("Fail, not a path!!! ")
            return src
    except:
        print("Failed to build a path!")
        return src


def LoadListSelector(List_Path):
    """
    Load a list and prompt the user to select a TV Show Or Movie.

    depends on:
        imports:
            os
            inquirer
            re

    :param List_Path: path to the list file.
    :return: an array of Show Name, Show folder parant path
    """
    try:
        if (os.path.isfile(List_Path)):  # Make sure the file exists
            with open(List_Path) as Lines:  # Read the file
                # read the contets of the file and split into lines
                Show_List_Unsplit = Lines.read().splitlines()
            Show_List_Names = []  # Set a blank array for the show list
            Show_List_Full = []  # Set a blank array for the show list
            for L in Show_List_Unsplit:  # Loop threw the list lines
                Show_List_Names.append(re.split(r' : ', L)[0])
                Show_List_Full.append(re.split(r' : ', L))
            ques = [inquirer.List(
                'Show', message="Please select the TV show / Movie:", choices=Show_List_Names)]  # Built the question
            ans = inquirer.prompt(ques)  # prompt the user
            # Loop threw the list to find the index and full data coresponeding the user selection
            for i in range(len(Show_List_Full)):
                # Check if the current position is the user selection, if true go in.
                if Show_List_Full[i][0] == ans['Show']:
                    # Set the return value to the full data as an array.
                    ret = Show_List_Full[i]
                    break  # stop the loop
            return ret  # return the full data
        else:
            # Did not get a file.
            print("Not a Media list file!")
            return []
    except:
        # Error Out
        print("Failed to load list!")
        return []


# Set Flags and Argumanrs
def Set_Flags_Args(CleanUP, LoadList, Move, NewSName, Organaize, ReName, Source, MFsfx, MFSsfx, LFsfx, SFpfx):
    """
    Load a list and prompt the user to select a TV Show Or Movie.

    depends on:
        imports:
            os
        Functions:
            Val_SRC
            Org_TV_Movie
            Get_Files_In_Show_Folder
            Val_One_TV_Movie
            Val_List_File
            LoadListSelector
            Build_New_Path
            Check_SRC_DST

    :param CleanUP: True or Flase - Sets remove the main dir as part of the cleanup.
    :param LoadList: None if not used, Path string to a list file if used.
    :param Move: Move the files to new location, Empty if no, None if user did not provide manual path, Path if user provided
    :param NewSName: User provided name to use as a new name for the media. None if not provided, string if provided
    :param Organaize: True or False - if organaizeing is requested.
    :param ReName: True or False - if renameing is requested.
    :param Source: path string to folder of media files.
    :return: returns an array of all the params
    """
    # Initialize all the flags
    src = ""                # Path to source folder
    RM_MasDir = False       # Delete user provided path - No by defalut
    Use_List = False        # Use external list provided by user - No by default
    List_Valid = False      # List provided by user is good - No by Default
    List_Path = ""          # Empty string for the path to the list file
    Move_Files = False      # Move the files to new location
    Move_Path = ""          # The path to move the files
    ReN = False             # Rename media - defaults to No
    NewName = NewSName      # Place holder for the New name for the media
    OneSM = False           # One TV Show or One Movie in the folder to work on, defaults to No
    Files_In_Dir = []       # Setblank file array
    Org = False             # Organaized, False by default
    Answ = False            # Blank array to return
    No_Cont = False         # Set to false until a fail

    try:
        # Check source folder is a path to a folder
        if (os.path.isdir(Source)):
            # Check if the source folder conatins media files
            if (Val_SRC(Source, MFsfx, MFSsfx)):
                # Set the src to the source media folder
                src = Source
            else:
                # Not a media folder
                No_Cont = True
        else:
            # Not a folder
            No_Cont = True
        # Organaize The Source Folder
        if (Organaize and not No_Cont):
            Org = Org_TV_Movie(src, MFsfx, MFSsfx, LFsfx, SFpfx)
            No_Cont = True
        # Make sure no stop condition
        if (not No_Cont):
            # Get the file list
            Files_In_Dir = Get_Files_In_Show_Folder(src, MFsfx, MFSsfx)
            # Check if only One TV Show Or Movie is inside the source folder
            OneSM = Val_One_TV_Movie(
                Files_In_Dir, MFsfx, MFSsfx, LFsfx)
            # Set RM_MasDir to True if user whants to delete the main path as part of the cleanup
            if (CleanUP):
                RM_MasDir = True
            # Check if external media list provided, and if it is a valid list
            if (LoadList != None):
                Use_List = True  # User provided a media list file path
                # Validat the file, if valid set the List_Path to the path provided and it's validity to True
                if (Val_List_File(LoadList)):
                    List_Path = LoadList
                    List_Valid = True
                    # Print line Space
                    print("")
                    # Get The Show list and selext one
                    Selected_Show = LoadListSelector(List_Path)
                    # Overwrite the manual user input for the TV Show name
                    NewName = Selected_Show[0]
                    # check if user requested a move
                    if (Move != "Empty" and OneSM):
                        # Set the Move flag to true
                        Move_Files = True
                        # Save the location to move the show at the end
                        Move_Path = Build_New_Path(
                            Selected_Show[1], Selected_Show[0])
            # Check if user requested a name change
            if ((ReName or (Use_List and List_Valid))):
                # Set Rename flag to true
                ReN = True
            # Check if files need to move and set params acordingly
            if (Move != "Empty" and not (Use_List and List_Valid) and Move != None and NewName != ""):
                # Set the Move flag to true
                Move_Files = True
                # Save the location to move the show at the end
                Move_Path = Build_New_Path(Move, NewName)
            # Deal with / missing in src and not dst or Vise Versa
            src = Check_SRC_DST(src, Move_Path)
        # Return the answer
        Answ = True
    except:
        # Error out
        Answ = False

    # Return the results
    return [Answ, src, Org, OneSM, RM_MasDir, Use_List, List_Valid, List_Path, ReN, NewName, Move_Files, Move_Path, Files_In_Dir]


# Validate List File
def Val_List_File(List_Path):
    """
    Validate if the path is a valid TV Show and / or Movie File

    depends on:
        imports:
            os
            re

    :param List_Path: path to media list file to check
    :return: True if a valid file, false in any other case
    """
    try:
        # Check if the path is for a file
        if (os.path.isfile(List_Path)):
            with open(List_Path) as Lines:  # Read the file
                # read the contets of the file and split into lines
                Show_List_Unsplit = Lines.read().splitlines()
            Show_List_Names = []  # Set a blank array for the show list
            Show_List_Pathes = []  # Set a blank array for the show list
            for L in Show_List_Unsplit:  # Loop threw the list lines
                # Build a list of media names
                Show_List_Names.append(re.split(r' : ', L)[0])
                # Build a list of media folder pathes
                Show_List_Pathes.append(re.split(r' : ', L)[1])
            # Check if ther is at list one TV Show or Movie on the list, with at list one path
            if (len(Show_List_Names) > 0 and len(Show_List_Pathes) > 0):
                # Valid media list file
                return True
            else:
                # Not a valid media list file
                return False
        else:
            # the path is not a file
            return False
    except:
        # Error out
        return False


# Validate source folder
def Val_SRC(Source, MFsfx, MFSsfx):
    """
    Validate if the path is a valid TV Show and / or Movie folder

    depends on:
        imports:
            os
        functions:
            Get_Files_In_Show_Folder

    :param Source: path to media list folder to check
    :param MFsfx: suffix of media files to check for
    :param MFSsfx: suffix of subtitle files to check for
    :return: True if a valid path with at least one media file, false in any other case
    """
    try:
        # Check if the path is a directory
        if (os.path.isdir(Source)):
            # Check ther are sutiable media files in the directory
            if (Get_Files_In_Show_Folder(Source, MFsfx, MFSsfx)[0] != "Empty"):
                # Source path is valid
                return True
            else:
                # Not a media folder
                return False
        else:
            # Not a directory
            return False
    except:
        # Error out
        return False
