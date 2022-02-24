#!/usr/bin/python3

#Dependencies
import argparse
import requests
import random
import json
import yaml
import io
from collections import namedtuple
import os.path
import sys
from colorama import Fore,Back,Style
from yaml import tokens


#arguments
print(Fore.YELLOW)
parser = argparse.ArgumentParser(description='IDOR Automation Tool by WhitehatJr Security Team. Configure your yaml file as required to work with this tool.',epilog='Use responsibly, Enjoy pentesting')
parser.add_argument('-v', '--version', action='version', version='v1')
parser.add_argument('-gc', '--gen-config', action='store_true', help='Use this to generate new configuration file in case the older one is corrupted.')
#parser.add_argument('-cf', '--config_file', action='store',   help='provide other configuration file than default.')


#variables
cfilename = "idorconfig.yaml" 

#Config generation
def confgen():
    cfiledata = """
---
#Optional details about user.
user_details:
    role: teacher
    user_id: abc22-22
    user_name: khavs

#Static Authorization config. 
authorization:
    type: bearer
    token: abcxyz

#Cross user and Cross role test config. Dynamic tokens
tokens:
    another_teachers_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlblZlcnNpb24iOm51bGwsImlkIjoiZDU2NWVlYjItN2M5MC00NTY5LWIxMzctMjRhNWY4YTEwZGQ4IiwidG9rZW5UeXBlIjoicHJpbWFyeV90b2tlbiIsImV4cCI6MTYzOTIwNTM2OCwiaWF0IjoxNjMxNDI5MzY4fQ.uegGPONqo5TXvhwJ5P4v_uUIzTmfHUhfH7J0nfLMXHU
    std_token: vvvvss233
    admin_token: 34e3sd
    std_cum_teacher_token: sdfs33434

#Delay in seconds after each request.
delay:
    time: 0
"""

    cfile = open(cfilename, "w")
    cfile.write(cfiledata)
    cfile.close()
        

#Config override prompt function if argument passed
def confgen_arg():       
    if os.path.isfile(cfilename):
        answer = input("You already have a configuration file in the working directory. Would you like to override it.\n[y/n]: ") 
        if answer.lower() == "y" or answer.lower == "yes" :
            confgen()
            print("New configuration generated successfully")
        elif answer.lower() == "n" or answer.lower() == "no": 
            pass
        else: 
            print("Please enter y or n.")
            
#Config validation check
args = parser.parse_args()
if args.gen_config:
    confgen_arg()
else:
    pass

#Config Existence check 
print(Fore.CYAN+"Check1:")
print(Fore.CYAN+"Checking for configuration file.")
if not os.path.isfile(cfilename):
    confgen()
    print(Fore.YELLOW+"It looks you don't have configuration file. New configuration file " +cfilename+" has been generated successfully")
    print()
else:
    print(Fore.YELLOW+"You are good to go.")
    print()

    
#yaml to json conversion
yaml_file= open(cfilename, 'r')
json_file = yaml.safe_load(yaml_file)

# Return tokens and token count
total_tokens= len(json_file['tokens'])
all_tokens= json_file['tokens']


#tokens validation check fuction
def token_validation(token):
    url= "https://stage-api.whjr.one/api/V1/userDetail/me"
    method= "get"
    body= {"age":"22"}
    headers= {"Authorization": "Bearer " +token}
    response = getattr(requests,method)(url,headers=headers)
    token_name= list(all_tokens.keys())[token_number]
    if response.status_code != 200:
        print(Fore.YELLOW+"ERROR: " +token_name+ " doesn't have a valid token assigned. Please check again your configuration file, "+cfilename)
        print()


# mass endpoint authorization check
def auth_check(tes_turl, test_method, test_headers):
    test_response = getattr(requests,test_method)(test_url,headers=test_headers)
    if test_response.status_code != 200:
        print(Back.GREEN+Fore.WHITE + token_name+ Style.RESET_ALL+ Fore.GREEN +" doesn't have access to " +test_url+ " endpoint")
        print()
    elif test_response.status_code == 200:
        print(Back.RED+Fore.WHITE + token_name+ Style.RESET_ALL+Fore.RED + " has access to " +test_url+ " endpoint")
        print()


#Check validation of tokens
print(Fore.CYAN+"Check2: ")
print(Fore.CYAN+"Checking for token validation in configuration file.")
print()
token_number=0
while token_number < total_tokens:  
    token_value= list(all_tokens.values())[token_number]
    token_validation(token_value)
    token_number += 1
token_number=0


#Endpoint Auth check
print(Fore.CYAN+"Check3:")
print(Fore.CYAN+"Checking for broken authorization on all endpoints.")
print()
token_number=0
while token_number < total_tokens:  
    token_value= list(all_tokens.values())[token_number]
    token_name= list(all_tokens.keys())[token_number]
    test_url= "https://stage-api.whjr.one/api/V1/bookings/students/42e0723a-cea3-4ff5-b41e-2f563b7c29b3/getClasses"
    test_method= "get"
    test_body= {"age":"22"}
    test_headers= {"Authorization": "Bearer " + token_value}
    auth_check(test_url,test_method,test_headers)
    token_number += 1
token_number=0

