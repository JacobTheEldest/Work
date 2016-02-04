#! /usr/bin/python

'''
This module contains functions common to nadernet's browser automation scripts.
Created in order to begin conforming to the Unix Philosophy.
'''

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def element_exists(browser, identifier, method='xpath'):
    '''
    Returns True if it can find the specified element.
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
        elif method == 'link':
            element = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located((By.LINK_TEXT, identifier))
            )
    except:
        return False
    return True

def wait_for_element(browser, identifier, method='xpath', max_secs=60):
    '''
    Waits for an element to exist for 'max_secs' seconds
    '''
    wait = True
    count = 0
    while wait and count < max_secs:
        wait = not element_exists(browser, identifier, method)
        count += 1
    if wait:
        print('{}: {} cannot be found.'.format(method, identifier))
    return

def url_wait(browser, url):
    '''
    Continuously attempt to open a url until it succeeds.
    '''
    while True:
        try:
            browser.get(url)
        except:
            continue
        break

def login_info(filename='login'):
    '''
    Looks for a file called "login" in current directory. line1:user, line2:pass
    If no file exists asks for user input.
    '''
    if os.path.isfile(filename):
        login_file = open(filename)
        login_data = login_file.readlines()
        username = login_data[0][:-1]
        password = login_data[1][:-1]
    else:
        username = input('Username: ')
        password = getpass.getpass('Password: ')
    return (username, password)
