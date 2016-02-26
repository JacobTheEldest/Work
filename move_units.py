#! /usr/bin/python

'''
This scraper will pull info from NaderNet.
Usage: ./move_units.py filename department department
'''

import os
import sys
from nadernet import *
from selenium_jacob import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#Initial setup and menu control
def main():
    '''
    Move units to a department if they aren't already there.
    Input is a file of uids and/or serials. One per line.
    '''
    #Open Firefox
    global browser
    browser = webdriver.Firefox()
    #Open Nadernet, login, Manage UID
    nadernet_initialize(browser)

    #Get filenames
    if len(sys.argv) < 2:
        input_file = ask_filename('in')
        output_file = ask_filename('out')
    else:
        if sys.argv[1][0].lower() == 'm' and len(sys.argv[1]) == 13:
            temp_file = open('uid_temp', 'w')
            temp_file.write('{}\n'.format(sys.argv[1]))
            temp_file.close()
            input_file = open('uid_temp')
            output_file = open('cli_only_results', 'a')
        else:
            input_file = open(sys.argv[1])
            output_file = open('{}_results'.format(sys.argv[1]), 'w')

    #Get destination department
    move_options = ['cancel', 'unit disposition', 'data device entry',
                    'system test', 'system repair', 'add to inventory',
                    'scrap teardown', 'system teardown']
    if len(sys.argv) > 2:
        destination = ''
        for term in sys.argv[2:]:
            destination += term
            if term != sys.argv[-1]:
                destination += ' '
    else:
        destination = ''
    while destination.lower() not in move_options:
        print('Move to:')
        print('  1.\tUnit Disposition')
        print('  2.\tData Device Entry')
        print('  3.\tSystem Test')
        print('  4.\tSystem Repair')
        print('  5.\tAdd to Inventory')
        print('  6.\tScrap Teardown')
        print('  7.\tSystem Teardown')
        print('  0.\tCancel')
        destination = move_options[int(input('\n>>> '))]

    if destination.lower() == 'cancel':
        exit

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

    #Iterate through input file and move each unit
    for line in input_file.readlines():
        #skip empty lines
        if line == '' or line == '\n':
            continue
        #Ensure that all input ends in a newline
        if not line[-1] == '\n':
            line = line + '\n'

        #Enter the input into NaderNet
        search(browser, line)

        #Give it time to load
        wait_for_element(browser, scanbox_submit_id, 'id')

        #Handle output when the search returns an error
        if element_exists(browser, error_id, 'id'):
            print('{} not found.'.format(line[:-1]))
            output_file.write('{} not found.\n'.format(line[:-1]))
            continue

        #Give it time to load
        wait_for_element(browser, unit_details_options_id, 'id')

        #Go to Disposition step
        browser.find_element_by_xpath(disposition_button_xpath).click()
        #Give it time to load
        wait_for_element(browser, change_disp_button_id, 'id')

        #Check current Disposition
        browser.find_element_by_xpath(current_disp_xpath).text
        if destination.lower() == browser.find_element_by_xpath(current_disp_xpath) and browser.find_element_by_xpath(completed_xpath).text.lower() != 'completed':
            print('{} is already in {}'.format(line[:-1], destination))
            output_file.write('{} is already in {}\n'.format(line[:-1], destination))
            continue

        #Open menu, select destination, and click submit
        browser.find_element_by_id(change_disp_menu_id).click()
        browser.find_element_by_xpath(change_disp_input_xpath).send_keys(destination + '\n')
        browser.find_element_by_id(change_disp_button_id).click()
        #Give it time to load
        wait_for_element(browser, change_disp_button_id, 'id')

        #Handle output when the Item cannot be moved and returns an error
        if element_exists(browser, error_id, 'id'):
            print('{} cannot be moved.'.format(line[:-1]))
            output_file.write('{} cannot be moved.\n'.format(line[:-1]))
            continue

        print('Moved {} to {}'.format(line[:-1], destination))
        output_file.write('Moved {} to {}\n'.format(line[:-1], destination))

    #Cleanup
    input_file.close()
    output_file.close()
    browser.quit()
    if os.path.isfile('uid_temp'):
        os.remove('uid_temp')

#Ask for input filename
def ask_filename(type='in'):
    '''
    Returns file object .
    '''
    while True:
        filename = input('\nFilename ({}): '.format(type))
        if os.path.isfile(filename) and type == 'in':
            return open(filename)
        elif type == 'out':
            if os.path.isfile(filename):
                print('\nAppending to: {}'.format(filename))
            return open(filename, 'a')
        else:
            print('Invalid filename.\n')

#Call main() function
if __name__ == '__main__':
    main()
