import sys
import datetime
import csv
from os import path

""""
This section describes all functions called when the program is started.
"""
def startup():
    create_date_file()
    create_bought_file()
    create_sold_file()

def create_date_file():
    """Check if there is already a file present containing the date set as current date. If not: create one."""
    if path.exists('date.txt') == False:
        date = str(datetime.date.today())
        file = open('date.txt', 'w')
        file.write(date)
        file.close()
        
def create_bought_file():
    """Check if there is already a bought.csv file present. If not: create one"""
    if path.exists('bought.csv') == False:
        with open('bought.csv', 'w', newline='') as csvfile: 
            bought_creation = csv.writer(csvfile)
            bought_creation.writerow(['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date'])

def create_sold_file():
    """Check if there is already a sold.csv file present. If not: create one"""
    if path.exists('sold.csv') == False:
        with open('sold.csv', 'w', newline='') as csvfile: 
            sold_creation = csv.writer(csvfile)
            sold_creation.writerow(['id', 'bought_id', 'sell_date', 'sell_price'])


