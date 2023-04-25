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
Ver = "0.4.6-alpha"
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
                # Get The Show list and selext one
                Selected_Show = Get_List(args.LoadList)
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
                if ((args.ReName or args.Move) and OneSM):  # Rename If User Asked To
                    Rename_TV_Movie(f, ANew_Name)
                # Move To Correct Location
                if ((args.Move == None or args.Move) and OneSM):
                    # Make Sure args.Move Has a / at the end when src has it
                    if (args.Move != None):
                        if (not args.Move.endswith("/") and src.endswith("/") and args.Move != "Empty"):
                            args.Move = args.Move + "/"
                    # If dst set by external list use it, else if the user supplied new destination use it insted, if no new location don't move
                    if (dst != src):
                        Move_Media(New_Path, dst, MoT,
                                   Season_Folder_Prefix, Seas)
                    elif (args.Move != "Empty" and dst == src and args.Move != src):
                        Move_Media(New_Path, args.Move, MoT,
                                   Season_Folder_Prefix, Seas)
            # Meesege the user about renaming
            if (args.ReName and OneSM and (args.Move == "Empty" or (args.Move != "Empty" and dst == src))):
                print("Media Renamed!")
            # Meesege the user about renaming and moveing
            if ((args.Move == None or args.Move) and OneSM and args.Move != "Empty"):
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


# Make sure to run only if called directly
if __name__ == "__main__":
    main()
