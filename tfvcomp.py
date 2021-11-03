import os
import csv
import time
import json
from os.path import exists
from os.path import expanduser
import sys

class tfvcomp():

    tfvj = ".tfvars.json"

    #dm = 1 # dev mode
    dm = 0 # prod mode

    # get number of files gieven
    n = len(sys.argv)-1


    # check all the files specified exist in the current vars folder
    def checkexist(files):
        # prepend vars - if not currently in vars folder
        v = "vars/" if not str(os.getcwd()).endswith("vars") else ""

        # check and print filenames
        for file in files:
            if not exists(v + file + tfvcomp.tfvj):
                raise ValueError("File not found: " + file)
        return

    def createoutput(files):

        # output parent folder naming
        if tfvcomp.dm:
            parent = "/home/andrew/dev/tfvars_compare/testoutput"
        else:
            parent = expanduser("~")+"/tfvcomp"
        
        # create folder - if it doesn't exist already
        if not os.path.exists(parent):
            os.makedirs(parent)

        # output file path
        if tfvcomp.dm:
            ofn_prefix = "tfvars_compare"
            ofn_timestamp = time.strftime("%Y%m%d-%H%M%S")
            ofn_fileextension = ".csv"
            tfvcomp.outputfilepath = parent + "/" + ofn_prefix + ofn_fileextension
        else:
            ofn_prefix = "tfvars_compare_"
            ofn_timestamp = time.strftime("%Y%m%d-%H%M%S")
            ofn_fileextension = ".csv"
            tfvcomp.outputfilepath = parent + "/" + ofn_prefix + ofn_timestamp + ofn_fileextension


        # create csv file
        with open(tfvcomp.outputfilepath, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # header row
            # variable header
            vh = "Variable"
            writer.writerow([vh]+files)

    def appendvariables(files):
        # full file names array
        files = [file + tfvcomp.tfvj for file in files]

        # merge all files into one json with first elements 
        python_object = {} #empty
        for file in files:
            f = open(file,)
            python_object[file.replace(tfvcomp.tfvj,"")]=json.load(f)
            json_dump = json.dumps(python_object)

        # "make sure all files have the same variables declared"
        # create an exhaustive list (outer join) of files variablaes
        variables_outer_join = []
        for file in python_object:
            for variable in python_object[file]:
                # if it doesn't already exist in v_o_j then add it
                if variable not in variables_outer_join:
                    variables_outer_join.append(variable)
        
        # loop through exhaustive variables list
        for var in variables_outer_join:
            row = [] # clear row
            row.append(var) # variable name column
            
            # loop through each file, adding in corresponding variable value
            for file in python_object:
                # this try will attempt to access the variable
                try:
                    if type(python_object[file][var]) is list:
                        # if its a list then join all the elements with a comma
                        row.append(', '.join(python_object[file][var]))
                    else:
                        # otherwise put the variable in the row
                        row.append(python_object[file][var])
                except:
                    # if there is no variable then put a "-" in place
                    row.append("-")

            # then write each row to the file
            with open(tfvcomp.outputfilepath, 'a', newline='') as file:
                csv.writer(file).writerow(row)

        print("tfvcomp: file written to " + tfvcomp.outputfilepath)