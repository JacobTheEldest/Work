#!/usr/bin/python

'''
This scraper will pull info from NaderNet.
'''

import os
import getpass
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#Initial setup and menu control
def main():
    #Ask for login info
    #username = input('Username: ')
    #password = getpass.getpass('Password: ')
    username = 'jacobs'
    password = 'Drummer1'

    #Open Firefox
    browser = webdriver.Firefox()
    #browser.implicitly_wait(10)


    #LOGIN
    time.sleep(5)
    browser.get('web01.marrc.int/login')
    
    #Wait until login box appears
    print('Looking for username box')
    wait_element('/html/body/form/div[3]/div/div/div/div/div[3]/div[1]/div/div[1]/fieldset/label[1]/span/input')

    #login elements
    username_element = browser.find_element_by_id('tbLoginUsername')
    password_element = browser.find_element_by_id('tbLoginPassword')


    #login
    username_element.send_keys('{}'.format(username))
    password_element.send_keys('{}'.format(password))
    password_element.send_keys(Keys.ENTER)
    time.sleep(1)


    browser.get('http://web01.marrc.int/Admin/MaintainUnit')
    wait_element('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[5]/div/div/div/div/div/input')

    #Menu
    option = ''
    while option.lower() != 'q':
        print('\n\nChoose an option:')
        print('1.\tRetrieve info')
        print('2.\tMove Units')
        print('q\tQuit')
        
        option = input('\n')
        if option == '1':
            #Get filenames
            input_file = ask_input()
            output_file = ask_output()
            print('\n\n')
            
            #Retrieve info for lines in input file. Write to output file.
            retrieve_info(input_file, output_file)
            
            #Close files
            input_file.close()
            output_file.close()
        elif option == '2':
            #Get filename
            input_file = ask_input()
            print('\n\n')
            
            #Move Units
            move_units(input_file)
            
    #Cleanup
    browser.quit()

#Convert filenames to filepaths
def convert_to_filepath(filename):
    filepath = os.path.join(os.getcwd(), filename)    
    return filepath
    
#Retrieve UID, Serial, and Commodity from a list of UIDs and Serials
#Input is a file of uids and/or serials. One per line.
def retrieve_info(input_file, output_file):
    #Iterate through input file and retrieve info
    for line in input_file.readlines():
        #Ensure that all input ends in a newline
        if not line[-1] == '\n':
            line = line + '\n'
            
        #Enter the input into NaderNet 
        search(line)
        
        #Give it time to load
        time.sleep(1)
        
        #Handle output when the search returns an error
        if error_exists():
            print('{} Not found.'.format(line[:-1])) # immediate cli feedback for line's status
            if line[0].lower() == 'm' and len(line) == 14 and '-' in line:
                uid = line[:-1]
                serial = 'Unknown'
                commodity = 'Unknown'
                write_output(uid, serial, commodity)
            else:
                uid = 'Unknown'
                serial = line[:-1]
                commodity = 'Unknown'
                write_output(uid, serial, commodity)
            continue
            
        #Grab and format info from Nadernet into a list (info)
        info_element = browser.find_element_by_xpath('//*[@id="cphMainBody_viewUnitDetail"]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/h6')
        info = info_element.text
        info = info.split(' ')
        
        #Parse info list into appropriate variables for use
        uid = info[0]
        if 'Serial:' not in info:
            serial = 'Unknown'
        elif 'removed' in info[-1].lower():
            serial = 'Unknown'
        else:
            serial = info[-1]
        if 'Commodity:' in info:
            commodity = info[3]
        else:
            commodity = 'Unknown'
            
        #write uid, serial, and commodity to file
        write_output(uid, serial, commodity)

#Write to file in specific format
def write_output(col1, col2, col3):
    output_file.write('{}\t{}\t{}\n'.format(col1, col2, col3))

#Search for serial or UID
def search(term):
    scanbox = browser.find_element_by_id('cphMainBody_tbSearch')
    scanbox.clear()
    scanbox.send_keys(term)

#Look for error box
def element_exists(xpath):
    '''
    Returns True if it can find an error box in a NaderNet page.
    '''
    try:
        #xpath = "/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[3]/div/div"
        error_id = "cphMainBody_pnlError"
        error_element = browser.find_element_by_xpath(xpath)
    except:
        return False
    return True
    
#Wait until element can be found
def wait_element(xpath):
    wait = True
    while wait:
        wait = not element_exists(xpath)

#Ask for input filename
def ask_input():
    '''
    Returns input file.
    '''
    while True:
        filename = input('\nInput filename: ')
        if filename == '':
            filename = 'input.txt'
        filepath = convert_to_filepath(filename)
        if os.path.exists(filepath):
            break
        else:
            print('Invalid filename.\n')
    return open(filepath)
    
#Ask for input filename
def ask_output():
    '''
    Returns output file.
    '''
    filename = input('Output filename: ')
    if filename == '':
        filename = 'output.txt'
    filepath = convert_to_filepath(filename)
    if os.path.exists(filepath):
        print('\nAppending to: {}'.format(filename))
    return open(filepath, 'a')

#Move units to a department if they aren't already there
def move_units(input_file):
    
    #!!!Convert this to an array
    print('Move to:')
    print('1.\tUnit Disposition')
    print('2.\tData Device Entry')
    print('3.\tSystems Test')
    print('4.\tSystems Repair')
    print('5.\tAdd to Inventory')
    print('6.\tScrap Teardown')
    destination = input('\n')
    
    #Parse destination
    if destination == '1':
        destination = 'unit disposition'
    elif destination == '2':
        destination = 'data device entry'
    elif destination == '3':
        destination = 'system test'
    elif destination == '4':
        destination = 'system repair'
    elif destination == '5':
        destination = 'add to inventory'
    elif destination == '6':
        destination = 'scrap teardown'
    else:
        print('Invalid choice.')
        exit
    
    #Iterate through input file and move each unit
    for line in input_file.readlines():
        #Ensure that all input ends in a newline
        if not line[-1] == '\n':
            line = line + '\n'
            
        #Enter the input into NaderNet 
        search(line)
        
        #Give it time to load
        time.sleep(1)
        
        #Handle output when the search returns an error
        if element_exists('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[3]/div/div'):
            print('{} Not found.'.format(line[:-1])) # immediate cli feedback for line's status
            if line[0].lower() == 'm' and len(line) == 14 and '-' in line:
                uid = line[:-1]
                serial = 'Unknown'
                commodity = 'Unknown'
                write_output(uid, serial, commodity)
            else:
                uid = 'Unknown'
                serial = line[:-1]
                commodity = 'Unknown'
                write_output(uid, serial, commodity)
            continue
            
        #Go to Disposition step
        disposition_button = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[1]/div/div/ul/li[4]/a/span/span/span')
        disposition_button.click()
        
        #Give it time to load
        time.sleep(2)
        
        #Check current Disposition
        current_disp = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div/div/span/span[2]').text
        if destination == current_disp.lower():
            print('{} is already in {}'.format(line[:-1], destination))
        else:
            #dropdown = WebDriverWait(browser, 10).until(EC.presence_of_element_located(browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div/div/div/input')))
            dropdown = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div')
            dropdown.click()
            time.sleep(1)
            
            #disposition_box = WebDriverWait(browser, 10).until(EC.presence_of_element_located(browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div/div/div/input')))
            disposition_box = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div/div/div/input')
            disposition_box.send_keys('{}\n'.format(destination))
            
            submit_button = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/a')
            submit_button.click()
        time.sleep(2)

#Call main() function    
if __name__ == '__main__':
    main()
