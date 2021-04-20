# Imports
import sys
import datetime
import csv
import argparse
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from os import path
from tkcalendar import Calendar, DateEntry
from matplotlib import pyplot as plt

"""The following other Python files used in this program. """
import transactions #contains functions used to perform the transactions
import reports #contains functions used to create the reports
import helper #general helper functions
import startup #functions that are used when starting SuperPy for the first time
import subwindows #contains the functions used to expand the user interface with new windows
from subwindows import set_date #importing this function allows it to be used on the home screen of the interface
from helper import get_date #importing this function allows it to be used on the home screen of the interface

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.

"""
The section below describes all parsers, the elements used to communicate with the command line.
"""

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', help='Welcome to SuperPy. Please choose your command from the following items, or use one of the optional arguments below.')

parser.add_argument('-t', '--advance_time', type=int, metavar='', help='Advance time n days. Please specify the number of days with this argument')
parser.add_argument('-o', '--open_interface', action='store_true', help='Open the user interface')

sell_parser = subparsers.add_parser("sell", help='Sell an item')
buy_parser = subparsers.add_parser("buy", help='Buy an item')
report_parser = subparsers.add_parser("report", help='Create a report')

buy_parser.add_argument('--product_name', type=str, metavar='', required = True, help='Enter name of the bought product')
buy_parser.add_argument('--price', type=float, metavar='', required = True, help='Enter price of the bought product. Use decimal point ( . ) if needed.')
buy_parser.add_argument('--expiration_date', type=str, metavar='', required = True, help='Enter expiration date of the bought product in YYYY-mm-dd format')
buy_parser.add_argument('--buy_date', type=str, default='today', metavar='', required = False, help='Enter buy date of the bought product in YYYY-mm-dd format')

sell_parser.add_argument('--product_name', type=str, metavar='', required = True, help='Enter name of the sold product')
sell_parser.add_argument('--price', type=float, metavar='', required = True, help='Enter price of the sold product. Use decimal point ( . ) if needed.')

report_subparsers = report_parser.add_subparsers(dest='command', help='What kind of report would you like?')
report_inventory = report_subparsers.add_parser('inventory', help='Create a report of the inventory on a certain date. Use with "-h" to see options.')
report_revenue = report_subparsers.add_parser('revenue', help='Calculate revenue for a certain date or period. Use with "-h" to see options.')
report_profit = report_subparsers.add_parser('profit', help='Calculate profit for a certain date or period. Use with "-h" to see options.')

report_inventory.add_argument('--now', action='store_true', help='Show current inventory')
report_inventory.add_argument('--yesterday', action='store_true', help='Show yesterday\'s inventory')
report_inventory.add_argument('--date', type=str, help='Show inventory on date using YYYY-mm-dd format')
report_revenue.add_argument('--today', action='store_true', help='Show today\'s revenue')
report_revenue.add_argument('--yesterday', action='store_true', help='Show yesterday\'s revenue')
report_revenue.add_argument('--date', type=str, help='Show revenue on a specific date using YYYY-mm-dd format')
report_revenue.add_argument('--period', type=str, help='Show revenue for a specific period (YYYY-mm-dd/YYYY-mm-dd)') #Deze nog maken
report_profit.add_argument('--today', action='store_true', help='Show today\'s profit')
report_profit.add_argument('--yesterday', action='store_true', help='Show yesterday\'s profit')
report_profit.add_argument('--date', type=str, help='Show profit for a specific year (YYYY), month, (YYYY-mm) of day (YYYY-mm-dd)')
report_profit.add_argument('--period', type=str, help='Show profit for a specific period (YYYY-mm-dd/YYYY-mm-dd)') #deze nog maken
args = parser.parse_args()


"""
The functions below are needed for the (optional) user interface to function properly.
"""

def open_interface():
    """
    This function describes the main window, with the buy/sell/report options on the main screen.
    Additional windows are imported from the subwindows file if needed
    """
    window = Tk()
    window.title("SuperPy")
    date = get_date()
    lbl = Label(window, text="Welcome to SuperPy!")
    lbl.grid(column=0, row=0)
    lbl2 = Label(window, width=15, fg='red', text="Buy")
    lbl2.grid(column=0, row=1)
    lbl3 = Label(window, width=15,text="Product name")
    lbl3.grid(column=0, row=2, sticky=W)
    lbl4 = Label(window, width=15,text="Price")
    lbl4.grid(column=1, row=2, sticky=W)
    lbl5 = Label(window, width=15,text="Expiration date")
    lbl5.grid(column=2, row=2, sticky=W)
    buy_name = StringVar()
    buy_name_entry = ttk.Entry(window, width=10, textvariable=buy_name)
    buy_name_entry.grid(column=0, row=3)
    buy_price = StringVar()
    buy_price_entry = ttk.Entry(window, width=5, textvariable=buy_price)
    buy_price_entry.grid(column=1, row=3)
    buy_cal = DateEntry(window, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    buy_cal.grid(column=2, row=3)
    buy_cal.set_date(date)
    btn1 = Button(window, text="Buy product", command=lambda: command_buy_product(buy_name_entry, buy_price_entry, buy_cal, window))
    btn1.grid(column=3, row=3)
    blank1 = Label(window, width=15, fg='red', text=" ")
    blank1.grid(column=0, row=4, sticky=S)
    lbl6 = Label(window, width=15, fg='red', text="Sell")
    lbl6.grid(column=0, row=5, sticky=S)
    lbl7 = Label(window, width=15,text="Product name")
    lbl7.grid(column=0, row=6, sticky=W)
    lbl8 = Label(window, width=15,text="Price")
    lbl8.grid(column=1, row=6, sticky=W)
    item_list = helper.create_sell_items()
    items_for_sale = StringVar()
    items_for_sale.set(item_list[0])
    select_sell = OptionMenu(window, items_for_sale, *item_list)
    select_sell.grid(column=0, row=7)
    sell_price = StringVar()
    sell_price_entry = ttk.Entry(window, width=5, textvariable=sell_price)
    sell_price_entry.grid(column=1, row=7)
    btn2 = Button(window, text="Sell product", command=lambda: command_sell_product(items_for_sale, sell_price_entry, window))
    btn2.grid(column=2, row=7)
    blank2 = Label(window, width=15, fg='red', text=" ")
    blank2.grid(column=0, row=8, sticky=W)
    lbl9 = Label(window, width=15, fg='red', text="Report")
    lbl9.grid(column=0, row=9, sticky=W)
    button_inventory = Button(window, text="Inventory", command= lambda: subwindows.inventory_window(window))
    button_inventory.grid(column=0, row=10)
    button_revenue = Button(window, text="Revenue", command=lambda: subwindows.revenue_window(window))
    button_revenue.grid(column=1, row=10)
    button_profit = Button(window, text="Profit", command= lambda: subwindows.profit_window(window))
    button_profit.grid(column=2, row=10)
    blank3 = Label(window, width=15, fg='red', text=" ")
    blank3.grid(column=0, row=11, sticky=W)
    lbl10 = Label(window, width=15, fg='red', text="Date")
    lbl10.grid(column=0, row=12, sticky=W)
    lbl11 = Label(window, width=15, text="Current date")
    lbl11.grid(column=0, row=13, sticky=W)
    lbl12 = Label(window, width=15, text="Advance time\n(days)")
    lbl12.grid(column=1, row=13, sticky=W)
    lbl13 = Label(window, width=15, text="Advance time\n(select date)")
    lbl13.grid(column=4, row=13, sticky=W)
    date_label = Label(window, width=15, text=f"{date}") 
    date_label.grid(column=0, row=14, sticky=W)
    date_advance = StringVar()
    date_advance_entry = ttk.Entry(window, width=10, textvariable=date_advance)
    date_advance_entry.grid(column=1, row=14)
    button_date = Button(window, text="Submit", command=lambda: command_advance_time(date_advance_entry, window))
    button_date.grid(column=2, row=14)
    lbl14 = Label(window, width=15, text="or")
    lbl14.grid(column=3, row=14, sticky=W)
    date_select = Button(window, text="Select date", command=lambda: subwindows.select_date(window, 'advance_time'))
    date_select.grid(column=4, row=14)
    blank4 = Label(window, width=15, fg='red', text=" ")
    blank4.grid(column=0, row=15, sticky=W)
    lbl10 = Label(window, width=15, fg='red', text="Results\nlast week")
    lbl10.grid(column=0, row=16, sticky=W)
    last_week_r = Button(window, text="Last weeks revenue", command=lambda: subwindows.last_week('revenue'))
    last_week_r.grid(column=0, row=17)
    last_week_p = Button(window, text="Last weeks profit", command=lambda: subwindows.last_week('profit'))
    last_week_p.grid(column=1, row=17)
    window.mainloop()

def refresh_window(window):
    window.destroy()
    open_interface()
    
def command_buy_product(buy_name_entry, buy_price_entry, buy_cal, window):
    subwindows.buy(buy_name_entry, buy_price_entry, buy_cal)
    refresh_window(window)

def command_sell_product(items_for_sale, sell_price_entry, window): 
    product = items_for_sale.get()
    subwindows.sell(items_for_sale, sell_price_entry)
    refresh_window(window)

def command_advance_time(date_advance_entry, window):
    interval_box = date_advance_entry.get()
    if interval_box == '':
        messagebox.showerror("Error", "Please provide a number")
        return
    interval = int(interval_box)
    helper.advance_time(interval)
    date = get_date()
    messagebox.showinfo("Time travel!", f"Date set to {date}")
    refresh_window(window)

"""
End of the list of functions needed to run the user interface.
Below, under "if __name__ == '__main__': " are all possible conditions obtained from the command line with
their respective action using the functions described above.
The first line calls the startup() function, which checks for the presence of
the required date file and bought- and sold-items lists. 
"""

if __name__ == '__main__':
    startup.startup()
    if args.open_interface:
        open_interface()
    if args.command == 'buy':
        transactions.buy_item(args.product_name, args.price, args.expiration_date, args.buy_date)
        print('OK')
    if args.command == 'sell':
        transactions.sell_item(args.product_name, args.price)
        print('OK')
    if args.command == 'inventory':
        if args.now == True:
            date, date_upper_limit = helper.determine_period('now')
            reports.check_inventory(date)
        elif args.yesterday == True:
            date, date_upper_limit = helper.determine_period('yesterday')
            reports.check_inventory(date)
        elif args.date:
            date, date_upper_limit = helper.determine_period(args.date)
            reports.check_inventory(date)
        else:
            print('Please specify date. Use with "--now" for current inventory')
    if args.command == 'revenue':
        if args.today == True:          
            date, date_upper_limit = helper.determine_period('today')
            print(f'Today\'s revenue so far: {reports.revenue_period(date, date_upper_limit)}')
        elif args.yesterday == True:
            date, date_upper_limit = helper.determine_period('yesterday')
            print(f'Yesterday\'s revenue: {reports.revenue_period(date, date_upper_limit)}')
        elif args.date:
            date, date_upper_limit = helper.determine_period(args.date)
            if args.date.count('-') == 2:
                date_month = date.strftime("%B")
                print(f'Revenue from {date.day} {date_month} {date.year}: {reports.revenue_period(date, date_upper_limit)}')
            elif args.date.count('-') == 1:
                date_month = date.strftime("%B")
                print(f'Revenue from {date_month} {date.year}: {reports.revenue_period(date, date_upper_limit)}')
            elif args.date.count('-') == 0 and len(args.date) == 4:
                print(f'Revenue from {date.year}: {reports.revenue_period(date, date_upper_limit)}')
        elif args.period:
            date, date_upper_limit = helper.determine_period(args.period)
            print(f'Revenue from {args.period}: {reports.revenue_period(date, date_upper_limit)}')
        else:
            print('Please specify date or period. Use with "-h" to see options')
    if args.command == 'profit':
        if args.today == True:          
            date, date_upper_limit = helper.determine_period('today')
            print(f'Today\'s profit so far: {reports.profit(date, date_upper_limit)}')
        elif args.yesterday == True:
            date, date_upper_limit = helper.determine_period('yesterday')
            print(f'Yesterday\'s profit: {reports.profit(date, date_upper_limit)}')
        elif args.date:
            date, date_upper_limit = helper.determine_period(args.date)
            if args.date.count('-') == 2:
                date_month = date.strftime("%B")
                print(f'Profit from {date.day} {date_month} {date.year}: {reports.profit(date, date_upper_limit)}')
            elif args.date.count('-') == 1:
                date_month = date.strftime("%B")
                print(f'Profit from {date_month} {date.year}: {reports.profit(date, date_upper_limit)}')
            elif args.date.count('-') == 0 and len(args.date) == 4:
                print(f'Profit from {date.year}: {reports.profit(date, date_upper_limit)}')
        elif args.period:
            date, date_upper_limit = helper.determine_period(args.period)
            print(f'Profit from {args.period}: {reports.profit(date, date_upper_limit)}')
        else:
            print('Please specify date or period. Use with "-h" to see options')
    if args.advance_time:
        helper.advance_time(args.advance_time)
        date = get_date()
        print(f'Date adjusted with {args.advance_time} days. Current system date now {date}')

