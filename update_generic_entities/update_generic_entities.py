#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is meant to be executed with Python 3.
#
# To get more help, execute: "python3 ./update_generic_entities.py --help"
# 
# Before execute:
# - This script use a package that is not include in python ("requests"). You can install it with pip: "sudo pip install requests".
# - You must update the request body in this script to accomplish your purpose. Find the comment "UPDATE BODY" and proceed.
#
# Change url and entity
# Command to execute the script: "python3 ./update_generic_entities.py --file=input.csv --env=PROD"

import os
import sys

import csv
import json
import itertools
import requests

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_help():
    print (BColors.BOLD + "update_generic_entities help" + BColors.ENDC + """
    Generic script to do request to update entities. An output file is created when the script ends (output.csv).
    Allowed parameters are:
        --help:       Print the help message.
        --file:       Input CSV file.
        --env:        Environment: BETA or PROD. BETA is default

    Example:
    ./update_generic_entities.py --file=input.csv --env=PROD
    """)

Error = 0
OK = 0

def put_request(first_param, second_param, data, env):
    global Error, OK
    url = "http://changethisurl/"+env+"/entity/"+str(first_param)+"?param.id="+str(second_param)
    print (url)
    response = requests.put(url, data=data)

    if response.status_code != 200:
        print (BColors.FAIL + "Error updating: " + str(first_param) + " - second_param: " + str(second_param) + " - status: "+ str(response.status_code) + BColors.ENDC)
        print (response.text)
        Error += 1
    else:
        print (BColors.OKGREEN + "Update OK: " + str(first_param) + " - second_param: " + str(second_param) + BColors.ENDC)
        OK += 1
    return response


def safe_get(_list, index, default=None):
    if len(_list) > index:
        return _list[index]
    return default


if __name__ == "__main__":
    os.system('clear')
    
    params = {safe_get(elem.split("="), 0): safe_get(elem.split("="), 1) for elem in sys.argv[1:]}

    # Help command
    if "--help" in params.keys():
        print_help()
        sys.exit(0)

    get_from_file = '--file' in params.keys() and params['--file'] is not None
    get_env = '--env' in params.keys() and params['--env'] is not None

    if not get_from_file:
        print ("Must indicate the file path [--file]")
        sys.exit(1)

    env = 'url-beta'
    if not get_env or params['--env'].lower() == 'prod':
        env = 'url'

    if get_from_file and not os.path.exists(params['--file']):
        print ("The file specified is not valid")
        sys.exit(1)


    filename = params['--file']
    with open(filename, 'r') as f:
        cl_reader = csv.reader(f)
        file_data = [tuple(line) for line in cl_reader]
        
        print ("Found " + BColors.BOLD + str(len(file_data)) + BColors.ENDC + \
              " rows in the file " + BColors.BOLD + filename + BColors.ENDC)

        print ("executing update" + BColors.ENDC)

        # UPDATE BODY
        data = json.dumps({'first_property':'first_property','second_property': 'second_property'})


        with open('output.csv', 'a') as csvResult:
            writer = csv.writer(csvResult)
            writer.writerow(['first_param', 'status_code', 'details'])

            for data_row in file_data:
                first_param = data_row[0]
                second_param = data_row[1]
                response = put_request(first_param, second_param, data, env)

                writer.writerow([first_param, response.status_code, response.text])

        csvResult.close()

    f.close()
    print ("Updated "+ str(OK)+" successfully" + BColors.ENDC)
    print ("Error in "+str(Error)+" rows" + BColors.ENDC)
