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
parser.add_argument('-R', '-r', '--ReName', action='store_true',
                    help="Rename the TV show or Movie files.")
parser.add_argument('-M', '-m', '--Move',
                    help="Move the TV Show Episodes to the path provided.", nargs='?', default="Empty")
parser.add_argument('-L', '-l', '--LoadList',
                    help="Load external TV show list and select the correct one.")
args = parser.parse_args()

###############################
# Global Variables Defenition #
###############################

Ver = "0.2.0-2"     # Release number
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
            # Meesege the user
            print("Loaded all media and subtitle files to the program!")
            # Check If Path Contains Only On TV Show Or One Movie
            OneSM = Val_One_TV_Movie(
                Files_In_Dir, File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix)
            # Meesege the user
            if (OneSM):
                print("Only one TV Show or Movie Found!")
            # Check If External List Loaded and Use It (Make Sure Only  One TV Show Or Movie Present)
            if (args.LoadList != None and OneSM):
                # Get The Show list and selext one
                Selected_Show = Get_List(args.LoadList)
                # Overwrite the manual user input for the TV Show name
                NewName = Selected_Show[0]
                # Save the location to move the show at the end
                dst = Selected_Show[1]
                # Meesege the user
                print(
                    "External media list loaded, Media name Selected:", NewName)
            else:  # Make Sure NewName Is Not Set If Not Needed
                NewName = ""
            # Run threw each file
            for f in Files_In_Dir:
                # Get Season and Episde(s) for the file
                Seas, Epi = Get_Season_Episode(f)
                # Check If There Is A Season And Decide If It Is A Movie Or TV
                if (Seas == "Empty"):  # Movie
                    TVMName = Get_TV_Movie_Name(
                        f, "Movie", File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix)  # Get TV Or Movie Name
                    # If user supplied new name for the show or movie, Use it.
                    NewName = Val_New_Name(args.NewSName, TVMName, NewName)
                    # Get The Correct New Name And Path
                    ANew_Name, New_Path = Build_New_Name(
                        f, "", "", "Movie", NewName, Lang_File_Sufix, File_Sufix_Movies, File_Sufix_Subtitles)
                else:  # TV Show
                    TVMName = Get_TV_Movie_Name(
                        f, "TV", File_Sufix_Movies, File_Sufix_Subtitles, Lang_File_Sufix)  # Get TV Or Movie Name
                    # If user supplied new name for the show or movie, Use it.
                    NewName = Val_New_Name(args.NewSName, TVMName, NewName)
                    # Get The Correct New Name And Path
                    ANew_Name, New_Path = Build_New_Name(
                        f, Seas, Epi, "TV", NewName, Lang_File_Sufix, File_Sufix_Movies, File_Sufix_Subtitles)
                if (args.ReName and OneSM):  # Rename If User Asked To
                    Rename_TV_Movie(f, ANew_Name, TVMName, False)
                # Move To Correct Location
                if (args.Move != "Empty" and OneSM):
                    print("Move")
            # Meesege the user
            if (args.ReName and OneSM):
                print("Media Renamed!")
        else:
            # Error on path not valid
            print("Not A Valid Folder, quiting!!!")
    except:
        print("UnKnown Error!!!!")


# Make sure to run only if called directly
if __name__ == "__main__":
    main()
