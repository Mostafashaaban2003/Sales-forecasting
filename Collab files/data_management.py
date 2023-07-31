# ********************** imports Section Start **********************
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# ********************** imports Section End   **********************

# ********************** Global Variables Section Start **************
first_branch_sales = pd.read_csv('..\\Project dataset\\first branch.csv')
second_branch_sales = pd.read_csv('..\\Project dataset\\second branch.csv')
third_branch_sales = pd.read_csv('..\\Project dataset\\third branch.csv')
branch_sales = first_branch_sales
# ********************** Global Variables  Section End   *************

# to display a graph
def do_you_want_to_display_a_graph(period_sales, x, y):
    graph = input("\nDo you want to display a graph for this period?"
                  "\nEnter 1 for \"Yes\" and anything else for \"No\": ")
    if (graph != '1'):
        return
    plt.figure(figsize=(x, y))
    pl.plot(period_sales['date'], period_sales['sales'])
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.title("Customer Sales")
    plt.show()

def branch_selection():
    choice = input("Enter 1 for \"first branch\" or 2 for \"second branch\" or anything else for \"third branch\": ")
    if (choice == '1'):
        return first_branch_sales
    elif (choice == '2'):
        return second_branch_sales
    else:
        return third_branch_sales
def branch_selection_for_files():
    choice = input("Enter 1 for \"first branch\" or 2 for \"second branch\" or anything else for \"third branch\": ")
    if (choice == '1'):
        return '..\\Project dataset\\first branch.csv'
    elif (choice == '2'):
        return '..\\Project dataset\\second branch.csv'
    else:
        return '..\\Project dataset\\third branch.csv'

def to_monthly_sales(num_branch_sales, n):
    # converting date to a Month period
    monthly_sales = num_branch_sales
    monthly_sales['date'] = pd.to_datetime(monthly_sales['date'])
    monthly_sales['date'] = monthly_sales['date'].dt.to_period("M")
    # sum the number of items in each month
    monthly_sales = monthly_sales.groupby('date').sum().reset_index()
    # convert date to timestamp datatype
    monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()
    if(n == 1):
        monthly_sales['sales diff'] = monthly_sales['sales'].diff()
    else:
        sales_different = input("Do you want to display sales different between each month and the one before it ?"
                            "\nEnter 1 for \"Yes\" and anything else for \"No\": ")
        if(sales_different == '1'):
            monthly_sales['sales diff'] = monthly_sales['sales'].diff()
    #delete the rows with missing values
    monthly_sales = monthly_sales.dropna()
    return monthly_sales
def check_password(password):
    i = 0
    enteredpassword = input("Please enter your password: ")

    while(enteredpassword != password):
        print("INVALID PASSWORD.\n"
              "You Have", 3-i, " More Tries.\n")
        enteredpassword = input("Enter your password: ")
        i = i+1
        if(i == 3):
            exit()
def choose_number(n):
    while(True):
        choice = int(input())
        if(choice >= 1 and choice <= n):
            return choice
            break
        print("\nInvalid choice!\n"
              "please enter number between 1~", n, ": ")
