#!/usr/bin/python

'''
Scrapes aging report info from mrmprod.
'''

import os
import getpass
import requests

def main():
    #Ask for login info
    #username = input('Username: ')
    #password = getpass.getpass('Password: ')
    username = 'jacobs'
    password = 'Drummer1'
    
    session = requests.Session()
    payload = {'ctl00$ContentPlaceHolder1$Login$UserName': username, 'ctl00$ContentPlaceHolder1$Login$Password': password}
    session.post('http://mrmprod/Login.aspx', data=payload)

if __name__ == '__main__':
    main()
