#! /usr/bin/python

'''
This scraper will pull info from NaderNet.
'''

import os
import getpass
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#Initial setup and menu control
def main():
    #Retrieve login info
    (username, password) = login()

    #Open Firefox
    global browser
    browser = webdriver.Firefox()

    #LOGIN
    browser_load_wait('web01.marrc.int/login')
    #Login Page find elements
    username_id = 'tbLoginUsername'
    password_id = 'tbLoginPassword'
    submit_button_id = 'btnLogin'
    #Wait until login box appears
    wait_for_element(username_id, id)
    #Enter info and submit
    browser.find_element_by_id(username_id).send_keys('{}'.format(username))
    browser.find_element_by_id(password_id).send_keys('{}'.format(password))
    browser.find_element_by_id(submit_button_id).click()

    #Manage UID
    browser.get('http://web01.marrc.int/Admin/MaintainUnit')
    #Manage UID find elements
    scanbox_id = 'cphMainBody_tbSearch'
    scanbox_submit_id = 'cphMainBody_lbSearch'
    #Wait for search box to appear
    wait_for_element('id', scanbox_id)



    #Menu
    while True:
        option = ''
        print('\n\nChoose an option:')
        print('   1.\tRetrieve info')
        print('   2.\tMove Units')
        print('   q.\tQuit')

        #Parse options
        option = input('\n>>>  ')
        if option == '1':
            retrieve_info()

        elif option == '2':
            move_units()
        else:
            break

    #Cleanup
    browser.quit()

#Convert filenames to filepaths
def convert_to_filepath(filename):
    filepath = os.path.join(os.getcwd(), filename)
    return filepath

#Ask for login info
def login():
    #username = input('Username: ')
    #password = getpass.getpass('Password: ')
    username = 'jacobs'
    password = 'Drummer1'
    return (username, password)

#Continuously attempt to open a url until it succeeds.
def browser_load_wait(url):
    while True:
        try:
            browser.get(url)
        except:
            continue
        break

#Retrieve UID, Serial, and Commodity from a list of UIDs and Serials
#Input is a file of uids and/or serials. One per line.
def retrieve_info():
    #Get filenames
    input_file = ask_input()
    output_file = ask_output()
    print('\n\n')
    #Iterate through input file and retrieve info
    for line in input_file.readlines():
        #Mange UID find elements
        error_id = 'cphMainBody_pnlError'
        summary_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/h6'
        #Ensure that all input ends in a newline
        if not line[-1] == '\n':
            line = line + '\n'

        #Enter the input into NaderNet
        search(line)

        #Give it time to load
        time.sleep(1)

        #Handle output when the search returns an error
        if element_exists(error_id, 'id'):
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
        info = browser.find_element_by_xpath('//*[@id="cphMainBody_viewUnitDetail"]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/h6').text
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
        output_file.write('{}\t{}\t{}\n'.format(uid, serial, commodity))

    #Close files
    input_file.close()
    output_file.close()

#Search for serial or UID
def search(term):
    browser.find_element_by_id('cphMainBody_tbSearch').clear()
    browser.find_element_by_id('cphMainBody_tbSearch').send_keys(term)

#Look for element existence
def element_exists(identifier, method='xpath'):
    '''
    Returns True if it can find the specified element
    '''
    try:
        if method == 'xpath':
            element = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located((By.XPATH, identifier))
            )
        elif method == 'id':
            element = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located((By.ID, identifier))
            )
    except:
        return False
    return True

#Wait until element can be found
def wait_for_element(identifier, method='xpath'):
    wait = True
    count = 0
    while wait and count < 100:
        wait = not element_exists(identifier, method)
        count += 1
    return

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
def move_units():
    #Get filename
    input_file = ask_input()
    output_file = open('move_unit_results', 'w')
    print('\n\n')

    #Manage UID find elements
    summary_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[1]/h6'
    unit_details_options_id = 'cphMainBody_UnitDetailView_btnOptionButton'
    error_id = 'cphMainBody_pnlError'
    disposition_button_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[1]/div/div/ul/li[4]/a/span/span/span'
    change_disp_menu_id = 'cphMainBody_ChangeDispositionUC_lbDisposition_chosen'
    change_disp_input_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div/div/div/input'
    change_disp_button_id = 'cphMainBody_ChangeDispositionUC_linkChangeDisposition'
    current_disp_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div/div/span/span[2]'
    scanbox_submit_id = 'cphMainBody_lbSearch'
    completed_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div[6]/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div/div/span/span[1]'

    #show menu
    print('Move to:')
    print('   1.\tUnit Disposition')
    print('   2.\tData Device Entry')
    print('   3.\tSystem Test')
    print('   4.\tSystem Repair')
    print('   5.\tAdd to Inventory')
    print('   6.\tScrap Teardown')
    print('   7.\tSystem Teardown')
    print('   0.\tCancel')
    move_options = ['Cancel', 'Unit Disposition', 'Data Device Entry',
                    'System Test', 'System Repair', 'Add to Inventory',
                    'Scrap Teardown', 'System Teardown']
    destination = move_options[int(input('\n>>>  '))]

    if destination == 'Cancel':
        exit

    #Iterate through input file and move each unit
    for line in input_file.readlines():
        #skip empty lines
        if line == '' or line == '\n':
            continue
        #Ensure that all input ends in a newline
        if not line[-1] == '\n':
            line = line + '\n'

        #Enter the input into NaderNet
        search(line)

        #Give it time to load
        wait_for_element(scanbox_submit_id, 'id')

        #Handle output when the search returns an error
        if element_exists(error_id, 'id'):
            print('{} not found.'.format(line[:-1]))
            output_file.write('{} not found.'.format(line[:-1]))
            continue

        #Give it time to load
        wait_for_element(unit_details_options_id, 'id')

        #Go to Disposition step
        browser.find_element_by_xpath(disposition_button_xpath).click()
        #Give it time to load
        wait_for_element(change_disp_button_id, 'id')

        #Check current Disposition
        browser.find_element_by_xpath(current_disp_xpath).text
        if destination.lower() == browser.find_element_by_xpath(current_disp_xpath) and browser.find_element_by_xpath(completed_xpath).text.lower() != 'completed':
            print('{} is already in {}'.format(line[:-1], destination))
            output_file.write('{} is already in {}'.format(line[:-1], destination))
            continue
        #Open menu, select destination, and click submit
        browser.find_element_by_id(change_disp_menu_id).click()
        browser.find_element_by_xpath(change_disp_input_xpath).send_keys(destination + '\n')
        browser.find_element_by_id(change_disp_button_id).click()
        #Give it time to load
        wait_for_element(change_disp_button_id, 'id')

        #Handle output when the Item cannot be moved and returns an error
        if element_exists(error_id, 'id'):
            print('{} cannot be moved.'.format(line[:-1]))
            output_file.write('{} cannot be moved.'.format(line[:-1]))
            continue

        print('Moved {} to {}'.format(line[:-1], destination))
        output_file.write('Moved {} to {}\n'.format(line[:-1], destination))

    #cleanup
    input_file.close()
    output_file.close()

#Call main() function
if __name__ == '__main__':
    main()
