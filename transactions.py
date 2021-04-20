import helper
import sys
import datetime
import csv
from os import path

"""
The functions below are used by the program to perform the various transactions, either called for via the
command line, or using the user interface.
"""

def buy_item(product_name, buy_price, expiration_date, buy_date):
    """ The main action for buying a product. Requires a name, price, expiration date and date of purchase
    Generates a new ID based on the last know ID and stores all values in a csv file. """
    product_name = product_name.lower()
    with open('bought.csv', 'r+', newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        find_buy_id = [0]
        for row in reader:
            bought_id = int(row[0])
            find_buy_id.append(bought_id)
        bought_id = max(find_buy_id)+1
        if buy_date == 'today':
            date_bought = helper.get_date()
        else:
            date_bought = buy_date
        bought_item = csv.writer(file)
        bought_item.writerow([bought_id, product_name, date_bought, buy_price, expiration_date])

def sell_item(product_name, sell_price):
    """ The main action for selling a product.
    Requires a name and price and stores these values with the Buy-ID in a csv file. """
    date = helper.get_date()
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader) 
        sold_items_list = [line[1] for line in sold_reader] 
        find_sold_id = [0] 
        sold_file.seek(0) 
        next(sold_reader)
        for row in sold_reader:
            sold_id = int(row[0])
            find_sold_id.append(sold_id) 
        sold_id = max(find_sold_id)+1 #Determine the new sell_ID by taking the highest currently present ID and adding +1
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader)
        #Now the function checks for availability of the item: were there more products with this name bought than sold, and did these products not expire?
        stock = [line[0] for line in bought_reader if line[1] == product_name and datetime.datetime.strptime(line[4], "%Y-%m-%d").date() >= date and line[0] not in sold_items_list] #Creates a list of all items with that product name that are not expired nor sold
        if stock:
            bought_id = stock[0]
            with open('sold.csv', 'a', newline='') as sold_file:
                sold_item = csv.writer(sold_file)
                sold_item.writerow([sold_id, bought_id, date, sell_price])
        else:
            print('Item not in stock')

