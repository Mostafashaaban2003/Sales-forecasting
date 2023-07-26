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
#Read and save train.csv in first_branch_sales
first_branch_sales = pd.read_csv("first branch.csv")
second_branch_sales = pd.read_csv("second branch.csv")
thired_branch_sales = pd.read_csv("thired branch.csv")
#converting date from object datatype to dateTime datatype
first_branch_sales["date"]=pd.to_datetime(first_branch_sales["date"])
second_branch_sales["date"]=pd.to_datetime(second_branch_sales["date"])
thired_branch_sales["date"]=pd.to_datetime(thired_branch_sales["date"])

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
        year_sales = first_branch_sales.loc[(year - 2013) * 365 + constant - bool(year % 4 == 0): (year + 1 - 2013) * 365 + constant - 1]
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
                month_sales = first_branch_sales.loc[(year-2013)*365 + constant-1 + (month-1 - 2*bool(not(month <= 2)))*(30+bool(month <= 2)) + bool(not(month <= 2))*((month-1-bool(month < 8))/2) + bool(not(month <= 2))*((month-bool(month < 8))%2) + bool(not(month <= 2))*(58 + bool(year%4 == 0)) + bool(year%4 != 0): (year-2013)*365 + constant-1 + abs((2-month))*30 + bool(not(month <= 2))*(month-bool(month < 8))/2 + bool(month <= 2)*(58+bool(year%4 == 0))*abs(month-1) + bool((not(month<=2)))*(58+bool(year%4 == 0)) + bool(year%4 != 0)]
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
                print(first_branch_sales.loc[index_day])
                break
#to display a graph
def Do_you_want_to_display_a_graph(period_sales, x, y):
    plt.figure(figsize=(x, y))
    pl.plot(period_sales['date'], period_sales['sales'])
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.title("Customer Sales")
    plt.show()
    
#to display monthly sales and monthly sales difference  
    #converting date to a Month period
first_branch_sales['date']=first_branch_sales['date'].dt.to_period("M")
     #sum the number of items in each month
monthly_sales1=first_branch_sales.groupby('date').sum().reset_index()
    #convert date to timestamp datatype
monthly_sales1['date']=monthly_sales1['date'].dt.to_timestamp()
monthly_sales1['sales diff']=monthly_sales1['sales'].diff()
    #delete the rows with missing values
monthly_sales1=monthly_sales1.dropna() 

    #converting date to a Month period
second_branch_sales['date']=second_branch_sales['date'].dt.to_period("M")
    #sum the number of items in each month
monthly_sales2=second_branch_sales.groupby('date').sum().reset_index()
    #convert date to timestamp datatype
monthly_sales2['date']=monthly_sales2['date'].dt.to_timestamp()
monthly_sales2['sales diff']=monthly_sales2['sales'].diff()
    #delete the rows with missing values
monthly_sales2=monthly_sales2.dropna()

    #converting date to a Month period
thired_branch_sales['date']=thired_branch_sales['date'].dt.to_period("M")
    #sum the number of items in each month
monthly_sales3=thired_branch_sales.groupby('date').sum().reset_index()
    #convert date to timestamp datatype
monthly_sales3['date']=monthly_sales3['date'].dt.to_timestamp()
monthly_sales3['sales diff']=monthly_sales3['sales'].diff()
    #delete the rows with missing values
monthly_sales3=monthly_sales3.dropna()

def disply_monthly_sales():
    choice = input("Enter 1 for \"first branch\" or 2 for \"second branch\" or 3 for \"thired branch\" or a for \"All\": ")
    if(choice=='1'):
      
        print(monthly_sales1)
    elif(choice=='2'):
       
        print(monthly_sales2)
    elif(choice=='3'):
       print(monthly_sales3)
    elif(choice=='a'):
        print("the first branch:")
        print(monthly_sales1)
        print("-"*50)
        print("the second branch:")
        print(monthly_sales2)
        print("-"*50)
        print("the thired branch:")
        print(monthly_sales3)
        
    else:
        print("unexpected value")
        disply_monthly_sales()
        
#to predict sales
def predict_sales():
        choice = input("Enter 1 for \"first branch\" or 2 for \"second branch\" or 3 for \"thired branch\" ")
        if(choice=='1'):
          supervised_data1=monthly_sales1.drop(['date','sales'],axis=1)
          for i1 in range(1,13):
              col_name1='month_'+str(i1)
              supervised_data1[col_name1]=supervised_data1['sales_diff'].shiht(i1)
          supervised_data1=supervised_data1.dropna().reset_index(drop=True)
          #split the data into train and test
          train_data1=supervised_data1[:-12]
          test_data1=supervised_data1[-12:]
          scaler1=MinMaxScaler(feature_range=(-1,1))
          scaler1.fit(train_data1)
          train_data1=scaler1.transform(train_data1)
          test_data1=scaler1.transform(test_data1)
          x_train1,y_train1=train_data1[:,1:],test_data1[:,0:1]
          x_test1,y_test1=test_data1[:,1:],test_data1[:,0:1]
          
          
          
            
        # elif(choice=='2'):
           
            
        # elif(choice=='3'):
           
        
            
        # else:
        #     print("unexpected value")
        #     disply_monthly_sales()
