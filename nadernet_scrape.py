#!/usr/bin/python

'''
This scraper will pull info from NaderNet.
'''

import sys
import os
import getpass
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


#VARIABLE ASSIGNMENT
#Retrieve and assign any arguments
if len(sys.argv) > 1:
    input_filename = sys.argv[1]
else: 
    input_filename = 'input.txt'
if len(sys.argv) > 2:
    output_filename = sys.argv[2]
else: output_filename = 'output.txt'

input_filepath = os.path.join(os.getcwd(), input_filename)
output_filepath = os.path.join(os.getcwd(), output_filename)

#Make sure input file exists
if not os.path.exists(input_filename):
    print('Please rerun with a valid input file.')
    exit

#Filename info for user
print('Input file:  {}'.format(input_filename))
if os.path.exists(output_filepath):
    print('Appending to output file: {}'.format(output_filename))
else:
    print('Output file: {}'.format(output_filename))

#open files
input_file = open(input_filepath)
output_file = open(output_filepath, 'a')
in_lines = input_file.readlines()


#Ask for login info
#username = input('Username: ')
#password = getpass.getpass('Password: ')
username = 'jacobs'
password = 'Drummer1'

#Open Firefox
browser = webdriver.Firefox()

#LOGIN
time.sleep(5)
browser.get('web01.marrc.int')
#login elements
username_element = browser.find_element_by_id('tbLoginUsername')
password_element = browser.find_element_by_id('tbLoginPassword')


#login
username_element.send_keys('{}'.format(username))
password_element.send_keys('{}'.format(password))
password_element.send_keys(Keys.ENTER)


browser.get('http://web01.marrc.int/Admin/MaintainUnit')
time.sleep(1)

def error_exists():
    try:
        xpath = "/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[3]/div/div"
        error_id = "cphMainBody_pnlError"
        error_element = browser.find_element_by_id(error_id)
    except:
        return False
    return True
    
#!!!BEGIN RETRIEVAL
for line in in_lines:
    #Ensure that all input ends in a newline
    if not line[-1] == '\n':
        line = line + '\n'
        
    #Enter the input into NaderNet 
    scanbox = browser.find_element_by_id('cphMainBody_tbSearch')
    scanbox.clear()
    scanbox.send_keys(line)
    
    time.sleep(1)
    
    #Detect errorbox when item not found
    if error_exists():
        print('{} Not found.'.format(line[:-1])) # immediate cli feedback for line's status
        if line[0].lower() == 'm' and len(line) == 14 and '-' in line:
            output_file.write('{}\tUnknown\n'.format(line[:-1]))
        else:
            output_file.write('Unknown\t\t{}\n'.format(line[:-1]))
        continue
    
    info_element = browser.find_element_by_xpath('//*[@id="cphMainBody_viewUnitDetail"]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/h6')
    print('{} found.'.format(line[:-1])) # immediate cli feedback for line's status
    
    #Grab and format info from Nadernet
    info = info_element.text
    info = info.split(' ')
    uid = info[0]
    
    #Check Serial Number existence and integrity
    if 'Serial:' not in info:
        serial = 'Unknown'
    elif 'removed' in info[-1].lower():
        serial = 'Unknown'
    else:
        serial = info[-1]
    output_file.write('{}\t{}\n'.format(uid, serial))

#Cleanup
browser.close()
input_file.close()
output_file.close()
