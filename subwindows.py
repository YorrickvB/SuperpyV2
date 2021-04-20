import helper
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
from helper import get_date
import transactions
import reports

"""
The functions below are used to create new windows in the user interface. New windows are required to either
ask for additional imput or to further specify the type of operation desired by the user. 
"""

def buy(buy_name_entry, buy_price_entry, buy_cal):
    """This function is called when the 'Buy item' button on the home screen is pressed. It registers the buying
    of a new item"""
    product = buy_name_entry.get()
    if product == '':
        messagebox.showerror("Error", "Please provide a valid name")
        return
    price_box = buy_price_entry.get()
    if price_box == '':
        messagebox.showerror("Error", "Please provide a valid price")
        return
    price = float(price_box)
    ex_date =  buy_cal.get_date()
    buy_date = get_date()
    transactions.buy_item(product, price, ex_date, buy_date)
    messagebox.showinfo("Bought!", f"{product} bought for {price}!")

def sell(items_for_sale, sell_price_entry):
    """This function is called when the 'Sell item' button on the home screen is pressed. It registers sale
    of an item"""
    product = items_for_sale.get()
    if product == 'Select item':
        messagebox.showerror("Error", "Please select item to sell")
        return
    price_box = sell_price_entry.get()
    if price_box == '':
        messagebox.showerror("Error", "Please provide a valid price")
        return
    price = float(price_box)
    transactions.sell_item(product, price)
    messagebox.showinfo("Sold!", f"{product} sold for {price}!")
    
def last_week(command):
    """An extra feature of the main screen: to provide insight in last week's financial results, two buttons
    are added: one for last week's profit, another for revenue. This function generates a bar graph with these stats"""
    date_upper_limit = get_date()
    date = date_upper_limit + datetime.timedelta(days = -6)
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)      
        dates_list = []
        revenue_list = []
        profit_list = []
        if command == 'revenue':
            while date <= date_upper_limit:
                dates_list.append(str(date.strftime('%a')))
                revenue = reports.revenue_period(date, date)
                revenue_list.append(revenue)
                date = date + datetime.timedelta(days = +1)
        elif command == 'profit':
            while date <= date_upper_limit:
                dates_list.append(str(date.strftime('%a')))
                daily_profit = reports.profit(date, date)
                profit_list.append(daily_profit)
                date = date + datetime.timedelta(days = +1)
        y_axis = revenue_list if command == 'revenue' else profit_list
        plt.bar(dates_list, y_axis)
        plt.title(f'Last weeks {command}')
        plt.xlabel("Date")
        plt.ylabel(f"{command}")
        plt.show()

"""
The functions below create a new, Toplevel window when more input is required to perform an action.
"""

def inventory_window(window):
    """#Creates a window to ask for more details on the inventory report"""
    inventory_screen = Toplevel(window)
    i_lbl = Label(inventory_screen, text="Select an option")
    date = get_date()
    yesterday = date + datetime.timedelta(days = -1)
    i_lbl.grid(column=0, row=0)
    i_btn1 = Button(inventory_screen, text="Now", command= lambda: messagebox.showinfo(f"Inventory on {date}", (reports.check_inventory(date))))  
    i_btn1.grid(column=0, row=1)
    i_btn2 = Button(inventory_screen, text="Yesterday", command= lambda: messagebox.showinfo(f"Inventory on {yesterday}", (reports.check_inventory(yesterday)))) 
    i_btn2.grid(column=1, row=1)
    i_btn3 = Button(inventory_screen, text="Select date", command= lambda: select_date(inventory_screen, 'inventory')) 
    i_btn3.grid(column=2, row=1)
    i_btn4 = Button(inventory_screen, text="Close screen", command= lambda: inventory_screen.destroy()) 
    i_btn4.grid(column=0, row=2)


def revenue_window(window):
    """Creates a window to ask for more details on the revenue report""" 
    revenue_screen = Toplevel(window)
    date = get_date()
    yesterday = date + datetime.timedelta(days = -1)
    r_lbl = Label(revenue_screen, text="Select an option")
    r_lbl.grid(column=0, row=0)
    r_btn1 = Button(revenue_screen, text="Today", command= lambda: messagebox.showinfo("Revenue", f'Today\'s revenue: {reports.revenue_period(date, date)}')) 
    r_btn1.grid(column=0, row=1)
    r_btn2 = Button(revenue_screen, text="Yesterday", command= lambda: messagebox.showinfo("Revenue", f'Yesterday\'s revenue: {reports.revenue_period(yesterday, yesterday)}')) 
    r_btn2.grid(column=1, row=1)
    r_btn3 = Button(revenue_screen, text="Select date", command= lambda: select_date(revenue_screen, 'revenue')) 
    r_btn3.grid(column=2, row=1)
    r_btn3 = Button(revenue_screen, text="Select period", command= lambda: select_period(revenue_screen, 'revenue')) 
    r_btn3.grid(column=3, row=1)
    r_btn5 = Button(revenue_screen, text="Close screen", command= lambda: revenue_screen.destroy()) 
    r_btn5.grid(column=0, row=2)

def profit_window(window):
    """Creates a window to ask for more details on the profit report"""
    profit_screen = Toplevel(window)
    date = get_date()
    yesterday = date + datetime.timedelta(days = -1)
    p_lbl = Label(profit_screen, text="Select an option")
    p_lbl.grid(column=0, row=0)
    p_btn1 = Button(profit_screen, text="Today", command= lambda: messagebox.showinfo("Profit", f'Today\'s profit: {reports.profit(date, date)}')) 
    p_btn1.grid(column=0, row=1)
    p_btn2 = Button(profit_screen, text="Yesterday", command= lambda: messagebox.showinfo("Profit", f'Yesterday\'s profit: {reports.profit(yesterday, yesterday)}')) 
    p_btn2.grid(column=1, row=1)
    p_btn3 = Button(profit_screen, text="Select date", command= lambda: select_date(profit_screen, 'profit')) 
    p_btn3.grid(column=2, row=1)
    p_btn4 = Button(profit_screen, text="Select period", command= lambda: select_period(profit_screen, 'profit')) 
    p_btn4.grid(column=3, row=1)
    p_btn5 = Button(profit_screen, text="Close screen", command= lambda: profit_screen.destroy()) 
    p_btn5.grid(column=0, row=2)    
  

def select_date(window, command):
    """Creates a new screen to ask for a specific date, linked to one of the actions.
    like changing the current date of specifying the desired date for one of the reports"""
    date_screen = Toplevel(window)
    d_lbl = Label(date_screen, text="Select prefered date")
    d_lbl.grid(column=0, row=0)
    d_lbl2 = Label(date_screen, width=15, text="Click here")
    d_lbl2.grid(column=0, row=1)
    cal = DateEntry(date_screen, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    cal.grid(column=0, row=2)
    current_date = get_date()
    cal.set_date(current_date)
    d_btn1 = Button(date_screen, text="Set date", command= lambda: [set_date(cal, command, window), date_screen.destroy()])
    d_btn1.grid(column=0, row=3)

def set_date(cal, command, window): 
    date = cal.get_date() 
    if command == 'inventory':
        messagebox.showinfo(f"Inventory on {date}", (reports.check_inventory(date)))
    if command == 'revenue':
        total_revenue = reports.revenue_period(date, date)
        messagebox.showinfo("Revenue", f"Total revenue on {date}: {total_revenue}")
    if command == 'profit':
        total_profit = reports.profit(date, date)
        messagebox.showinfo("Profit", f"Total profit on {date}: {total_profit}")
    if command == 'advance_time':
        date = str(date)
        file = open('date.txt', 'w')
        file.write(date)
        file.close()
        messagebox.showinfo("Time travel!", f"Date set to {date}")

def select_period(window, command):
    """Creates a new screen to ask for a specific period, linked to one of the actions.
    like specifying the desired period for one of the reports   """
    period_screen = Toplevel(window)
    d_lbl = Label(period_screen, text="Select prefered period")
    d_lbl.grid(column=0, row=0)
    d_lbl2 = Label(period_screen, width=15, text="From")
    d_lbl2.grid(column=0, row=1)
    cal1 = DateEntry(period_screen, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    cal1.grid(column=0, row=2)
    current_date = get_date()
    cal1.set_date(current_date)
    d_lbl2 = Label(period_screen, width=15, text="To")
    d_lbl2.grid(column=1, row=1)
    cal2 = DateEntry(period_screen, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    cal2.grid(column=1, row=2)
    cal2.set_date(current_date)
    d_btn1 = Button(period_screen, text="Set period", command= lambda: [set_period(cal1, cal2, command), period_screen.destroy()])
    d_btn1.grid(column=0, row=3)

def set_period(cal1, cal2, command): 
    date1 = cal1.get_date()
    date2 = cal2.get_date()
    if command == 'revenue':
        total_revenue = reports.revenue_period(date1, date2)
        messagebox.showinfo("Revenue", f"Total revenue for\n{date1} till {date2}: {total_revenue}")
    if command == 'profit':
        total_profit = reports.profit(date1, date2)
        messagebox.showinfo("Profit", f"Total profit for\n{date1} till {date2}: {total_profit}")   