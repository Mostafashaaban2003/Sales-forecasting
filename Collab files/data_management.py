# ********************** imports Section Start **********************
import os
import openpyxl
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import pylab as pl
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# ********************** imports Section End   **********************

# ********************** Global Variables Section Start **************
# Read and save train.csv in first_branch_sales
start_day = 0
first_branch_sales = pd.read_csv('..\\Project dataset\\first branch.csv')
second_branch_sales = pd.read_csv('..\\Project dataset\\second branch.csv')
third_branch_sales = pd.read_csv('..\\Project dataset\\third branch.csv')
branch_sales = first_branch_sales
# converting date from object datatype to dateTime datatype
#first_branch_sales["date"] = pd.to_datetime(first_branch_sales["date"])
#second_branch_sales["date"] = pd.to_datetime(second_branch_sales["date"])
#third_branch_sales["date"] = pd.to_datetime(third_branch_sales["date"])
# ********************** Global Variables  Section End   *************

# to display a graph
def do_you_want_to_display_a_graph(period_sales, x, y):
    graph = input("\nDo you want to display a graph for this month?"
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
    global start_day
    if (choice == '1'):
        start_day = 2013
        return first_branch_sales
    elif (choice == '2'):
        start_day = 2014
        return second_branch_sales
    else:
        start_day = 2015
        return third_branch_sales
def begin(month_sales):
    begin = input("Do you want to view all sales ?"
                  "\nEnter 1 for \"Yes\" and anything else for \"No\": ")
    if (begin == '1'):
        print(month_sales)
        do_you_want_to_display_a_graph(month_sales, 50, 10)
        return 1
    return 0
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

def branch_selection_for_files():
    choice = input("Enter 1 for \"first branch\" or 2 for \"second branch\" or anything else for \"third branch\": ")
    global start_day
    if (choice == '1'):
        start_day = 2013
        return '..\\Project dataset\\first branch.csv'
    elif (choice == '2'):
        start_day = 2014
        return '..\\Project dataset\\second branch.csv'
    else:
        start_day = 2015
        return '..\\Project dataset\\third branch.csv'