import sys
import datetime
import csv

"""
The functions below are general useful functions, used in multiple operations.
"""

def get_date():
    """General overall helpful function to determine the date stored as 'today'.
    Takes no argument, returns the current date"""
    with open('date.txt') as f:
        lines = f.readlines()
        current_date = datetime.datetime.strptime(lines[0], "%Y-%m-%d").date()
        return current_date

def advance_time(interval):
    """The function used to advance the date stored as 'today'.
    Takes the current date and adds the specified number of days."""
    current_date = get_date()
    new_date = str(current_date + datetime.timedelta(days = interval))
    file = open('date.txt', 'w')
    file.write(new_date)
    file.close()

def find_sold_items(date, date_upper_limit):
    """Helper function to find all find the Buy_ID's of products sold in a certain period."""
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)
        sold_items_id = [line[1] for line in sold_reader if date <= datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= date_upper_limit]
        return sold_items_id



def determine_period(time):
    """Helper function to identify the right time period to be used with the various functions, based on
    input from either the command line or the user interface"""
    date = get_date()
    date_upper_limit = date
    if time == 'today' or time == 'now':
        date_upper_limit = get_date()
    elif time == 'yesterday':
        date = date + datetime.timedelta(days = -1)
        date_upper_limit = date
    else: #following lines based on YYYY-mm-dd format, as required.
        resolution = time.count('-') #Check if either a year, year-month or year-month-day is specified
        if resolution == 2:  #for year-month-day
            date = datetime.datetime.strptime(time, "%Y-%m-%d").date()
            date_upper_limit = date
        elif resolution == 1: #for year-month
            date = datetime.datetime.strptime(time, "%Y-%m").date()
            date_upper_limit = date
            date_month = date.strftime("%B")
            #determine last day of the month, taking into account
            #possible 28 (feb non-leap year) 29 (feb leap year), 30 of 31 day possibilities.
            for i in range(31): 
                date_upper_limit = date_upper_limit + datetime.timedelta(days = +1)
                if date_upper_limit.month > date.month:
                    date_upper_limit = date_upper_limit + datetime.timedelta(days = -1)
                    break
        elif resolution == 0 and len(time) == 4: #if only a year is given
            date = datetime.datetime.strptime(time, "%Y").date()
            date_upper_limit = datetime.date(date.year, 12, 31)
        elif resolution == 4 and len(time) == 21: #if a certain period is given in format YYYY-mm-dd-YYY-mm-dd
            date = datetime.datetime.strptime(time[0:9], "%Y").date()
            date_upper_limit = datetime.datetime.strptime(time[10:21], "%Y").date()
    return date, date_upper_limit


def create_sell_items():
    """#Function used to create a list of items for sale, to help the user specify what has been sold.
    Only items in stock and with a suitable expiration date are shown."""
    date = get_date()
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)
        sold_list = [line[1] for line in sold_reader]
    with open('bought.csv', newline='') as bought_file: 
        bought_reader = csv.reader(bought_file)
        next(bought_reader)
        stock = [line[1] for line in bought_reader if datetime.datetime.strptime(line[4], "%Y-%m-%d").date() >= date and line[0] not in sold_list] #Creates a list of all items with that product name that are not expired nor sold
        stock = sorted(stock)
        unique_stock_names =["Select item"] #dubbele waarden verwijderen uit de lijst
        for i in stock:
            if i not in unique_stock_names:
                unique_stock_names.append(i)
                unique_stock = sorted(unique_stock_names)
    return unique_stock_names
