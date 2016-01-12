#!/usr/bin/python

'''
A program to perform various manipulations on excel spreadsheets.
'''

import openpyxl

#Load workbooks
master = openpyxl.load_workbook('master.xlsx')
print('Opened master.xlsx.')
info = openpyxl.load_workbook('info.xlsx')
print('Opened info.xlsx.')


for sheet in master.get_sheet_names():
    master_current_sheet = master.get_sheet_by_name(sheet)
    print('Opened {}'.format(sheet))
    
    for sheet2 in info.get_sheet_names():
        info_current_sheet = info.get_sheet_by_name(sheet2)
        info_uids = {}
        for row in range(1, info_current_sheet.get_highest_row()+1):
            uid = info_current_sheet['A{}'.format(row)].value
            if uid != None and uid.lower() != 'UID'.lower():
                info_uids[uid] = row
        
        for row in range(1, master_current_sheet.get_highest_row()+1):
            uid = master_current_sheet['A{}'.format(row)].value
            if uid in info_uids.keys():
                for col in ('B', 'C', 'D', 'E', 'F'):
                    if master_current_sheet['{}{}'.format(col, row)].value == None:
                        master_current_sheet['{}{}'.format(col, row)].value = info_current_sheet['{}{}'.format(col, info_uids[uid])].value
master.save('master.xlsx')
