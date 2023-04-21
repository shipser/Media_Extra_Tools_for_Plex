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
#parser.add_argument('-N', '-n', '--NewSName', help="New Name for the show")
# parser.add_argument('-O', '-o', '--Organaize', action='store_true',
#                    help="Organize the show - add a sub dir for Season (with number) and move the files inside, then rename based on the formating. make sure there are no subfolders inside!!")
# parser.add_argument('-R', '-r', '--ReName', action='store_true',
#                    help="Rename the main show folder.")
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

src = ""  # Place Holder For Source Folder

###################
# Start the Logic #
###################


# Main function to run
def main():
    try:
        TestFunc()
    except:
        print("Error!!!!")


# Make sure to run only if called directly
if __name__ == "__main__":
    main()
