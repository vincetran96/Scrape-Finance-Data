# THIS FILE IS USED FOR CONFIRMING THE INTEGRITY OF QUARTERS SCRAPED FROM VIETSTOCK BALANCE SHEETS
import json

file = 'Vietstock_BS_data_AAM.json'
with open('balance_sheets\{}'.format(file), encoding="utf-8") as jsonfile:
    text = json.load(jsonfile)
    for dic in text['data']:
        print (dic['quarter'])