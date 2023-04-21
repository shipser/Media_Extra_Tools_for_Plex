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

from Functions.Func import *    # Import all custom functions
import argparse                 # Imported for the arguments


############################
# Argument Parser Settings #
############################


parser = argparse.ArgumentParser(description="******************************************************************************************\nText Place Holder\n******************************************************************************************",
                                 usage='%(prog)s [OPTIONS]', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-S', '-s', '--Source', required=True,
                    help="Source directory of the TV Show or Movie. Required to operate!")
parser.add_argument('-N', '-n', '--NewSName',
                    help="New Name for the TV Show or Movie. Does not run if more then one TV Show or Movie if the path!")
# parser.add_argument('-O', '-o', '--Organaize', action='store_true',
#                    help="Organize the show - add a sub dir for Season (with number) and move the files inside, then rename based on the formating. make sure there are no subfolders inside!!")
parser.add_argument('-R', '-r', '--ReName', action='store_true',
                    help="Rename the TV show or Movie files.")
# parser.add_argument('-S', '-s', '--SeasonRename', action='store_true',
#                    help="Rename the season folder\s.")
# parser.add_argument('-M', '-m', '--Move',
#                    help="Move the TV Show Episodes to the path provided.", nargs='?', default="Empty")
# parser.add_argument('-L', '-l', '--LoadList',
#                    help="Load external TV show list and select the correct one.")
args = parser.parse_args()

###############################
# Global Variables Defenition #
###############################

Ver = "0.1.0-0"     # Release number
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
    try:
        # Make Sure the path is valid and get the files inside
        if (os.path.isdir(args.Source)):
            # Set Source Folder
            src = args.Source
            # Set Destination Folder
            dst = src
            # Get the file list
            Files_In_Dir = Get_Files_In_Show_Folder(
                src, File_Sufix_Movies, File_Sufix_Subtitles)
            # Check If Path Contains Only On TV Show Or One Movie
            OneSM = Val_One_TV_Movie(
                Files_In_Dir, File_Sufix_Movies, File_Sufix_Subtitles)
            # Run threw each file
            for f in Files_In_Dir:
                # Get Season and Episde(s) for the file
                Seas, Epi = Get_Season_Episode(f)
                # Check If There Is A Season And Decide If It Is A Movie Or TV
                if (Seas == "Empty"):  # Movie
                    TVMName = Get_TV_Movie_Name(
                        f, "Movie", File_Sufix_Movies, File_Sufix_Subtitles)  # Get TV Or Movie Name
                    # If user supplied new name for the show or movie, Use it.
                    NewName = Val_New_Name(args.NewSName, TVMName)
                    # Get The Correct New Name And Path
                    ANew_Name, New_Path = Build_New_Name(f, "", "", "Movie", NewName,
                                                         "", Lang_File_Sufix, File_Sufix_Movies, File_Sufix_Subtitles)
                else:  # TV Show
                    TVMName = Get_TV_Movie_Name(
                        f, "TV", File_Sufix_Movies, File_Sufix_Subtitles)  # Get TV Or Movie Name
                    # If user supplied new name for the show or movie, Use it.
                    NewName = Val_New_Name(args.NewSName, TVMName)
                    # Get The Correct New Name And Path
                    ANew_Name, New_Path = Build_New_Name(f, Seas, Epi, "TV", NewName,
                                                         Season_Folder_Prefix, Lang_File_Sufix, File_Sufix_Movies, File_Sufix_Subtitles)
                if (args.ReName and OneSM):  # Rename If User Asked To
                    Rename_TV_Movie(f, ANew_Name, File_Sufix_Movies)
                #print(NewName, " -> ", ANew_Name, " -> ", New_Path)
        else:
            # Error on path not valid
            print("Not A Valid Folder, quiting!!!")
    except:
        print("UnKnown Error!!!!")


# Make sure to run only if called directly
if __name__ == "__main__":
    main()
