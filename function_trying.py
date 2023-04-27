#!/usr/bin/env python3

import inquirer
import os
import re

li_pa = "/Users/shay/Downloads/TVShow.list"


def LoadListSelector(List_Path):
    """
    Load a list and prompt the user to select a TV Show Or Movie.

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


print(LoadListSelector(li_pa))
