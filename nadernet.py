#! /usr/bin/python

'''
This module contains functions common to nadernet's browser automation scripts.
Created in order to begin conforming to the Unix Philosophy.
'''

import os
import getpass
from selenium_jacob import *

def nadernet_initialize(browser):
    '''
    Initial startup, login, and go to Manage UID
    '''
    #LOGIN
    #Retrieve login info
    (username, password) = login_info('nadernet_login')
    #Open login page when browser loads
    url_wait(browser, 'web01.marrc.int/login')
    #login page elements identifiers
    username_id = 'tbLoginUsername'
    password_id = 'tbLoginPassword'
    submit_button_id = 'btnLogin'
    #Wait until login box appears
    wait_for_element(browser, username_id, id)
    #Enter info and submit
    browser.find_element_by_id(username_id).send_keys('{}'.format(username))
    browser.find_element_by_id(password_id).send_keys('{}'.format(password))
    browser.find_element_by_id(submit_button_id).click()

    #Go to Manage UID
    browser.get('http://web01.marrc.int/Admin/MaintainUnit')
    #Manage UID find elements
    scanbox_id = 'cphMainBody_tbSearch'
    scanbox_submit_id = 'cphMainBody_lbSearch'
    #Give it time to load
    wait_for_element(scanbox_id, 'id')

def search(browser, term):
    '''
    Search for term in Tag Search or Manage UID Search inputbox
    '''
    scanbox_id = 'cphMainBody_tbSearch'
    browser.find_element_by_id(scanbox_id).clear()
    browser.find_element_by_id(scanbox_id).send_keys(term)
    return
