import helper
import sys
import datetime
import csv
from os import path

"""
The functions below are used by the program to create the various reports, either called for via the
command line, or using the user interface.
"""

def check_inventory(time):
    """Function to check the inventory on a given moment, using one argument: the date that is requested.
    Result is stored as a separate csv file with name "Inventory {date}" and also printed on the command line"""
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader) 
        sold_items_list = [line[1] for line in sold_reader if datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= time] #Creates a list of ids for all items sold
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader) 
        stock = [[line[1].lower(), line[3], line[4]] for line in bought_reader if datetime.datetime.strptime(line[4], "%Y-%m-%d").date() > time and line[0] not in sold_items_list and datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= time] #Creates a list of all items that are not expired nor sold
        unique_stock =[]
        for i in stock:
            if i not in unique_stock:
                unique_stock.append(i)
                unique_stock = sorted(unique_stock)
        fields = ['Product name', 'Count', 'Buy Price', 'Expiration Date']
        with open(f'Inventory {time}.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(unique_stock)
        inventory = f'Inventory saved as Inventory {time}.csv \nProduct name \tCount \tBuy Price \tExpiration Date' #eindresultaat opmaken
        for row in unique_stock:
            inventory = inventory + f'\n{row[0]} \t\t{stock.count(row)} \t{row[1]} \t\t{row[2]}'
        print(inventory)
        return inventory

def revenue_period(date, date_upper_limit):
    """The main function to determine the revenue in a given period. Either one day, in which case both required
    arguments are equal, or a given period with a start and end date.
    Function returns the total revenue to the function that called it."""
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)
        sold_values = [float(line[3]) for line in sold_reader if date <= datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= date_upper_limit]
        total_revenue = sum(sold_values)
        return total_revenue


def profit(date, date_upper_limit):
    """The main function to determine the profit in a given period. Either one day, in which case both required
    arguments are equal, or a given period with a start and end date.Profit is determined by comparing the
    revenue in that period to the costs of buying all products that are sold in that period.
    Function returns the total profit to the function that called it."""
    total_revenue = revenue_period(date, date_upper_limit)
    sold_items_id = helper.find_sold_items(date, date_upper_limit)
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader) 
        costs = [float(line[3]) for line in bought_reader if line[0] in sold_items_id]
        total_costs = sum(costs)
        total_profit = total_revenue - total_costs
        return total_profit

