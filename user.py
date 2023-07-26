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
#Read and save train.csv in store_sales
store_sales_global = pd.read_csv("train.csv")

# ********************** Global Variables  Section End   *************

#function to display stationary data for user
def display_store_sales():

    choice = input("Enter 1 for \"Year\" or 2 for \"Month\" or anything else for \"Day\": ")
    #while(True) to get valid data
    while(True):
        year = int(input("Enter the year: "))
        if(year < 2018 and year > 2012):
            constant = int((year-2012) / 4)
            break

    if(choice == '1'):
        year_sales = store_sales_global.loc[(year - 2013) * 365 + constant - bool(year % 4 == 0): (year + 1 - 2013) * 365 + constant - 1]
        print(year_sales)
        graph = input("\nDo you want to display a graph for this year?"
                      "\nEnter 1 for \"Yes\" and anything else for \"No\": ")
        if (graph == '1'):
            Do_you_want_to_display_a_graph(year_sales, 450, 5)

    elif(choice == '2'):
        while(True):
            month = int(input("Enter the month: "))
            if (month > 12 or month <= 0):
                continue
            else:
                month_sales = store_sales_global.loc[(year-2013)*365 + constant-1 + (month-1 - 2*bool(not(month <= 2)))*(30+bool(month <= 2)) + bool(not(month <= 2))*((month-1-bool(month < 8))/2) + bool(not(month <= 2))*((month-bool(month < 8))%2) + bool(not(month <= 2))*(58 + bool(year%4 == 0)) + bool(year%4 != 0): (year-2013)*365 + constant-1 + abs((2-month))*30 + bool(not(month <= 2))*(month-bool(month < 8))/2 + bool(month <= 2)*(58+bool(year%4 == 0))*abs(month-1) + bool((not(month<=2)))*(58+bool(year%4 == 0)) + bool(year%4 != 0)]
                print(month_sales)
                graph = input("\nDo you want to display a graph for this month?"
                                  "\nEnter 1 for \"Yes\" and anything else for \"No\": ")
                if(graph == '1'):
                    Do_you_want_to_display_a_graph(month_sales, 40, 10)
                break

    else:
        while(True):
            month = int(input("Enter the month: "))
            if(month <= 12 or month > 0):
                break
        while(True):
            day = int(input("Enter the day: "))
            if(day <= 31 and day > 0):
                index_day = int((year - 2013) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0) - 1 + bool((month < 8 and month % 2 == 1) or (month >= 8 and month % 2 == 0)) + day)
                print(store_sales_global.loc[index_day])
                break
#to display a graph
def Do_you_want_to_display_a_graph(period_sales, x, y):
    plt.figure(figsize=(x, y))
    pl.plot(period_sales['date'], period_sales['sales'])
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.title("Customer Sales")
    plt.show()
