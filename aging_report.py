#!/usr/bin/python

'''
Scrapes aging report info from mrmprod.
'''

import os
import datetime
from selenium_jacob import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def main():
    #Retrieve login info
    (username, password) = login_info('makor_login')

    #Open Firefox
    #Give it time to load
    global browser
    browser = webdriver.Firefox()
    url_wait(browser, 'http://mrmprod/Login.aspx')

    #LOGIN
    #Login page find elements
    username_box_id = 'ctl00_ContentPlaceHolder1_Login_UserName'
    password_box_id = 'ctl00_ContentPlaceHolder1_Login_Password'
    login_submit_id = 'ctl00_ContentPlaceHolder1_Login_LoginButton'
    #Give it time to load
    wait_for_element(browser, username_box_id, 'id')
    browser.find_element_by_id(username_box_id).send_keys(username)
    browser.find_element_by_id(password_box_id).send_keys(password)
    browser.find_element_by_id(login_submit_id).click()

    #Aging Report
    summary_url = 'http://mrmprod/ProcessSteps/AssetRecoverySummary.aspx?LotNumber=-99&PageSize=999'
    skid_table_id = 'ctl00_CPH1_ResaleSummaryGrid_GridView1'
    browser.get(summary_url)
    wait_for_element(browser, skid_table_id, 'id')

    #Open output file
    now = datetime.datetime.now()
    output_file = open('{}-{}-{} {}-{} aging report'.format(now.year, now.month, now.day, now.hour, now.minute), 'w')
    output_file.write('Age\tLot\tClass\tAsset\tSerial\tManufacturer\tModel\tModel #\n')

    #Loop through the buttons for each skid
    num_skids = len(browser.find_elements_by_class_name('rbSecondary'))
    for button_num in range(0, num_skids):
        browser.get(summary_url)
        wait_for_element(browser, skid_table_id, 'id')
        process_button_els = browser.find_elements_by_class_name('rbSecondary')
        current_button_id = process_button_els[button_num].get_attribute('id')
        age = browser.find_element_by_id('{}lblDaysRecieved'.format(current_button_id[:-26])).text
        process_button_els[button_num].click()
        unit_table_id = 'ctl00_CPH1_ccTransGrid1_gvReceivingTransactions'
        wait_for_element(browser, unit_table_id, 'id')
        skid_url = browser.current_url

        num_units = len(browser.find_elements_by_xpath('/html/body/form/div[8]/div[13]/div[1]/div[1]/div/table/tbody//*[@value="Test"]'))
        num_pages = 1
        while True:
            if element_exists(browser, str(num_pages + 1), 'link'):
                num_pages += 1
            else:
                break
        for page in range(1, num_pages + 1):
            browser.get(skid_url)
            wait_for_element(browser, unit_table_id, 'id')
            if page != 1:
                browser.find_element_by_link_text(page)
                wait_for_element(browser, unit_table_id, 'id')
            for unit in range(0, num_units):
                test_button_els = browser.find_elements_by_xpath('/html/body/form/div[8]/div[13]/div[1]/div[1]/div/table/tbody//*[@value="Test"]')
                test_button_els[unit].click()
                asset_info_table_id = 'ctl00_CPH1_ccTransGrid1_rmaAssetInformation_fsAssetInfoControls'
                wait_for_element(browser, asset_info_table_id, 'id')

                lot_id = 'ctl00_CPH1_ccTransGrid1_DetailsHeader_lblLotNumber'
                unit_type_id = 'ctl00_CPH1_ccTransGrid1_rmaAssetInformation_lblClassName'
                asset_id = 'ctl00_CPH1_ccTransGrid1_rmaAssetInformation_lblAssetID'
                serial_id = 'ctl00_CPH1_ccTransGrid1_rmaAssetInformation_txtSerialNumber'
                manufacturer_id = 'ctl00_CPH1_ccTransGrid1_rmaAssetInformation_cmbManufacturers_Input'
                model_id = 'ctl00_CPH1_ccTransGrid1_rmaAssetInformation_cmbProducts_Input'
                model_num_id = 'ctl00_CPH1_ccTransGrid1_rmaAssetInformation_cmbProductNumbers_Input'

                lot = browser.find_element_by_id(lot_id).text
                unit_type = browser.find_element_by_id(unit_type_id).text
                asset = browser.find_element_by_id(asset_id).text
                serial = browser.find_element_by_id(serial_id).get_attribute('value')
                manufacturer = browser.find_element_by_id(manufacturer_id).get_attribute('value')
                model = browser.find_element_by_id(model_id).get_attribute('value')
                model_num = browser.find_element_by_id(model_num_id).get_attribute('value')

                output_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t\n'.format(age, lot, unit_type, asset, serial, manufacturer, model, model_num))


    #Cleanup
    output_file.close()

#Call main() function
if __name__ == '__main__':
    main()
