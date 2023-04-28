#!/usr/bin/env python3

##########################################################
##########################################################
## Writen By: Shay Pasvolsky | Apr 21st, 2023           ##
## Email: spasvolski@gmail.com                          ##
## GitHub: https://github.com/shipser                   ##
## Gitlab: @shipser                                     ##
## Licensce: GNU GPLv3                                  ##
##########################################################
##########################################################

###########
# Imports #
###########

from Functions.Func import *    # Import all custom functions
import argparse                 # Imported for the arguments


############################
# Argument Parser Settings #
############################

parser = argparse.ArgumentParser(description="******************************************************************************************\n\n  TV Show file renamer by Shay Pasvolsky (C).\n\n  The program acceptes only srt and mkv files!\n\n******************************************************************************************",
                                 usage='%(prog)s [OPTIONS]', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-C', '-c', '--CleanUp', action='store_true',
                    help="Remove source folder after moveing the media files, will only work if not other files or folders left inside.")
parser.add_argument('-L', '-l', '--LoadList',
                    help="Load external TV show list and select the correct one.")
parser.add_argument('-M', '-m', '--Move',
                    help="Move the TV Show Episodes or Movie to the path provided.", nargs='?', default="Empty")
parser.add_argument('-N', '-n', '--NewSName',
                    help="New Name for the TV Show or Movie. Does not run if more then one TV Show or Movie if the path!")
parser.add_argument('-O', '-o', '--Organaize', action='store_true',
                    help="Organize the Source directory!!")
parser.add_argument('-R', '-r', '--ReName', action='store_true',
                    help="Rename the TV show or Movie files.")
parser.add_argument('-S', '-s', '--Source', required=True,
                    help="Source directory of the TV Show or Movie. Required to operate!")
parser.add_argument('-V', '-v', '--Version', action='store_true',
                    help="Show the version number.")
args = parser.parse_args()


###############################
# Global Variables Defenition #
###############################

# Release number - Major.Minor.Fix, where fix can be uncomplited feature update
Ver = "1.0.1-RC2"
src = ""            # Place Holder For Source Folder
dst = ""            # Place Holder For Destination Folder
NewName = ""        # Place Holder For New TV Show Or Movie


###########################
# Do Not Change From Here #
###########################

# Show_Season_Dirs = []               # Seasons List
Files_In_Dir = []                   # File List
File_Sufix_Movies = ".mkv"          # Movie File Suffix
File_Sufix_Subtitles = ".srt"       # Movie File Suffix
Lang_File_Sufix = ".heb"            # Language Suffix For The Subtitles
Season_Folder_Prefix = "Season"     # Season folder prefix before the season number


###################
# Start the Logic #
###################

# Main function to run
def main():
    # Show The Version And Stop Running
    if (args.Version):
        Ver_String = "MET (Media Extra Tools for plex) Version: v" + Ver
        print(Ver_String)
        return True
    try:
        # Make Sure the path is valid and get the files inside
        if (os.path.isdir(args.Source)):
            # Set Source Folder
            src = args.Source
            # Set Destination Folder
            dst = src
            # Organaize The Source Folder
            if (args.Organaize):
                Org_TV_Movie(src, File_Sufix_Movies, File_Sufix_Subtitles,
                             Lang_File_Sufix, Season_Folder_Prefix)
            # Get the file list
            Files_In_Dir = Get_Files_In_Show_Folder(
                src, File_Sufix_Movies, File_Sufix_Subtitles)
            # Meesege the user
            print("Loaded all media and subtitle files to the program!")
            # Check If Path Contains Only On TV Show Or One Movie
            OneSM = Val_One_TV_Movie(
                Files_In_Dir, File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix)
            # Meesege the user
            if (OneSM):
                print("Only one TV Show or Movie Found, continueing!")
            # Check If External List Loaded and Use It (Make Sure Only  One TV Show Or Movie Present)
            if (args.LoadList != None and OneSM):
                # Print line Space
                print("")
                # Get The Show list and selext one
                Selected_Show = LoadListSelector(args.LoadList)
                # Overwrite the manual user input for the TV Show name
                NewName = Selected_Show[0]
                # Save the location to move the show at the end
                dst = Build_New_Path(Selected_Show[1], Selected_Show[0])
                # Meesege the user
                print(
                    "External media list loaded, Media name selected:", NewName)
            else:  # Make Sure NewName Is Not Set If Not Needed
                NewName = ""
            # Deal with / missing in src and not dst or Vise Versa
            src = Check_SRC_DST(src, dst)
            # Run threw each file
            for f in Files_In_Dir:
                # Get Season and Episde(s) for the file
                Seas, Epi = Get_Season_Episode(re.split(r'/', f)[-1])
                # Check If There Is A Season And Decide If It Is A Movie Or TV
                if (Seas == "Empty"):  # Movie
                    MoT = "Movie"  # Set Media Type For Futere Use
                    TVMName = Get_TV_Movie_Name(
                        f, MoT, File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix)  # Get TV Or Movie Name
                    # If user supplied new name for the show or movie, Use it.
                    NewName = Val_New_Name(args.NewSName, TVMName, NewName)
                    # Get The Correct New Name And Path
                    ANew_Name, New_Path = Build_New_Name(
                        f, "", "", MoT, NewName, Lang_File_Sufix, File_Sufix_Movies, File_Sufix_Subtitles)
                else:  # TV Show
                    MoT = "TV"  # Set Media Type For Futere Use
                    TVMName = Get_TV_Movie_Name(
                        f, MoT, File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix)  # Get TV Or Movie Name
                    # If user supplied new name for the show or movie, Use it.
                    NewName = Val_New_Name(args.NewSName, TVMName, NewName)
                    # Get The Correct New Name And Path
                    ANew_Name, New_Path = Build_New_Name(
                        f, Seas, Epi, MoT, NewName, Lang_File_Sufix, File_Sufix_Movies, File_Sufix_Subtitles)
                # Rename If User Asked To
                if ((args.ReName or args.Move != "Empty" or args.LoadList) and OneSM):
                    Rename_TV_Movie(f, ANew_Name)
                # Move To Correct Location
                if ((args.Move == None or args.Move != "Empty" or args.LoadList) and OneSM):
                    # Make Sure args.Move Has a / at the end when src has it
                    if (args.Move != None):
                        if (not args.Move.endswith("/") and src.endswith("/") and args.Move != "Empty"):
                            args.Move = args.Move + "/"
                    # If dst set by external list use it, else if the user supplied new destination use it insted, if no new location don't move
                    if (dst != src):
                        Move_Media(New_Path, Build_New_Path(dst, ANew_Name), MoT,
                                   Season_Folder_Prefix, Seas)
                    elif (args.Move != "Empty" and dst == src and args.Move != src):
                        Move_Media(New_Path, Build_New_Path(args.Move, ANew_Name), MoT,
                                   Season_Folder_Prefix, Seas)
            # Meesege the user about renaming
            if (args.ReName and OneSM and (args.Move == "Empty" or (args.Move != "Empty" and dst == src)) and not args.LoadList):
                print("Media Renamed!")
            # Meesege the user about renaming and moveing
            if ((args.Move == None or args.Move != "Empty" or args.LoadList) and OneSM):
                print("Media Renamed and Moved!")
                # Check if user requested to delete source folder and set the flag to true
                if (args.CleanUp):
                    rmsrc = True
                else:  # If user did not request to delete source folder, set the flage to false
                    rmsrc = False
                # Remove Empty Folders and tell the user it is done
                if (CleanUp_SRC(src, rmsrc)):
                    if (rmsrc):
                        print("Removed '{}' folder.".format(src))
                    else:
                        print("Removed empty folders inside '{}'".format(src))
                else:
                    print("Failed to delete empty folder(s)!")
            # Messege the user about Finishing
            print("Finished work!!")
        else:
            # Error on path not valid
            print("Not A Valid Folder, quiting!!!")
    except:
        print("UnKnown Error!!!!")


# New main loop
def main_New():
    # Set Falgs For The Jobs
    Run_The_Prog, src, Org, OneSM, RM_MasDir, Use_List, List_Valid, List_Path, ReN, NewNameUser, Move_Files, Move_Path, Files_In_Dir = Set_Flags_Args(
        args.CleanUp, args.LoadList, args.Move, args.NewSName, args.Organaize, args.ReName, args.Source, File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix, Season_Folder_Prefix)
    # Show The Version And Stop Running
    if (args.Version):
        Ver_String = "MET (Media Extra Tools for plex) Version: v" + Ver
        print(Ver_String)
        return True
    # Check if continue running
    if (Run_The_Prog and src != ""):
        # Make sure media files found
        if (Files_In_Dir != "Empty" and Files_In_Dir != "Error!!"):
            # Messege the user about finding files
            print("Found media files. loading the pathes to the program!")
            # Messege the user about organazing
            if (Org):
                print("Finished organaizing!")
            # Meesege the user ther is only one TV Show or Movie
            if (OneSM):
                print("Only one TV Show or Movie Found, continueing!")
                # Run threw each file
                for f in Files_In_Dir:
                    # Get Season and Episde(s) for the file
                    Seas, Epi = Get_Season_Episode(re.split(r'/', f)[-1])
                    # Check If There Is A Season And Decide If It Is A Movie Or TV
                    if (Seas == "Empty"):  # Movie
                        MoT = "Movie"  # Set Media Type For Futere Use
                        TVMName = Get_TV_Movie_Name(
                            f, MoT, File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix)  # Get TV Or Movie Name
                        # If user supplied new name for the show or movie, Use it.
                        NewName = Val_New_Name(NewNameUser, TVMName, NewName)
                        # Get The Correct New Name And Path
                        New_Name_Gen, New_Path = Build_New_Name(
                            f, "", "", MoT, NewName, Lang_File_Sufix, File_Sufix_Movies, File_Sufix_Subtitles)
                    else:  # TV Show
                        MoT = "TV"  # Set Media Type For Futere Use
                        TVMName = Get_TV_Movie_Name(
                            f, MoT, File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix)  # Get TV Or Movie Name
                        # If user supplied new name for the show or movie, Use it.
                        NewName = Val_New_Name(
                            NewNameUser, TVMName, NewNameUser)
                        # Get The Correct New Name And Path
                        New_Name_Gen, New_Path = Build_New_Name(
                            f, Seas, Epi, MoT, NewName, Lang_File_Sufix, File_Sufix_Movies, File_Sufix_Subtitles)
                    # Rename If User Asked To
                    if (ReN):
                        Rename_TV_Movie(f, New_Name_Gen)
                    # Move To Correct Location
                    if (Move_Files):
                        # If did not renam the file use the new path to the file
                        if (not ReN):
                            New_Path = f
                        # Move the file
                        Move_Media(New_Path, Build_New_Path(Move_Path, NewName), MoT,
                                   Season_Folder_Prefix, Seas)
                # Meesege the user about renaming
                if (ReN):
                    print("Media Renamed!")
                # Meesege the user about renaming and moveing
                if (Move_Files):
                    print("Media Moved!")
                    # Check if user requested to delete source folder and set the flag to true
                    if (RM_MasDir):
                        rmsrc = True
                    else:  # If user did not request to delete source folder, set the flage to false
                        rmsrc = False
                    # Remove Empty Folders and tell the user it is done
                    if (CleanUp_SRC(src, rmsrc)):
                        if (rmsrc):
                            print("Removed '{}' folder.".format(src))
                        else:
                            print("Removed empty folders inside '{}'".format(src))
                    else:
                        print("Failed to delete empty folder(s)!")
                # Messege the user about Finishing
                print("Finished all jobs!!")
                # Finish and exit
                return True
            else:
                #print("Use list: ", Use_List)
                #print("List is valid: ", List_Valid)
                #print("List path: ", List_Path)
                # Multi Show or Movies found
                print(
                    "No more jobs to do, Finished what is enabled for multi show media folder!")
                return False
        else:
            # No media files found in the path
            print("No media files found!!")
            return False
    else:
        # Error out
        print("Somthing went wrong!!!")
        return False


# Make sure to run only if called directly
if __name__ == "__main__":
    main_New()
