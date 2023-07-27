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
              supervised_data1[col_name1]=supervised_data1['sales diff'].shift(i1)
          supervised_data1=supervised_data1.dropna().reset_index(drop=True)
          #split the data into train and test
          train_data1=supervised_data1[:-12]
          test_data1=supervised_data1[-12:]
          
          scaler1=MinMaxScaler(feature_range=(-1,1))
          scaler1.fit(train_data1)
          train_data1=scaler1.transform(train_data1)
          test_data1=scaler1.transform(test_data1)
          
          x_train1,y_train1=train_data1[:,1:],train_data1[:,0:1]
          x_test1,y_test1=test_data1[:,1:],test_data1[:,0:1]
          y_train1=y_train1.ravel()
          y_test1=y_test1.ravel()
           #make prediction data frame
          sales_dates1=monthly_sales1['date'][-12:].reset_index(drop=True)
          predict_df1=pd.DataFrame(sales_dates1)
          act_sales1=monthly_sales1['sales'][-13:].to_list()
           #creat linear regression model and predicted output
          lr_model1=LinearRegression()
          lr_model1.fit(x_train1,y_train1)
          lr_pre1=lr_model1.predict(x_test1)
          
          lr_pre1=lr_pre1.reshape(-1,1)
           #matrix contains the output of the predicted data and test data input
          lr_pre_test_set1=np.concatenate([lr_pre1,x_test1],axis=1)
          lr_pre_test_set1=scaler1.inverse_transform(lr_pre_test_set1)
          
          result_list1=[]
          for index in range(0,len(lr_pre_test_set1)):
               result_list1.append(lr_pre_test_set1[index][0]+act_sales1[index])
          lr_pre_series1=pd.Series(result_list1,name='linear prediction')
          predict_df1=predict_df1.merge(lr_pre_series1,left_index=True,right_index=True)
          #Erorrs of prediction
          answer1=input("if you want to display errors of prediction press \"y\" if you don't press anything else: ")
          if answer1=="y":
           lr_mse1=np.sqrt(mean_squared_error(predict_df1['linear prediction'],monthly_sales1['sales'][-12:]))
           lr_mae1=mean_absolute_error(predict_df1['linear prediction'],monthly_sales1['sales'][-12:])
           lr_r2_1=r2_score(predict_df1['linear prediction'],monthly_sales1['sales'][-12:])
           print("Linear regression MSE:  ",lr_mse1)
           print("linear regression MAE: ",lr_mae1)
           print("linear regression R2: ",lr_r2_1 )
          answer_of_graph1=input("If you want to display the graph press \"y\" if you don't press anything else: ") 
          if answer_of_graph1=="y":
              plt.figure(figsize=(15,5))
              #actual sales
              plt.plot(monthly_sales1['date'],monthly_sales1['sales'])
              #predicted sales
              plt.plot(predict_df1['date'],predict_df1['linear prediction'])
              plt.xlabel('Date')
              plt.ylabel('Sales')
              plt.title('Sales forcasting')
              plt.legend(["Actual sales","Predicted sales"])
              plt.show()
           
           
            
        elif(choice=='2'):
             supervised_data2=monthly_sales2.drop(['date','sales'],axis=1)
             for i2 in range(1,13):
                 col_name2='month_'+str(i2)
                 supervised_data2[col_name2]=supervised_data2['sales diff'].shift(i2)
             supervised_data2=supervised_data2.dropna().reset_index(drop=True)
             #split the data into train and test
             train_data2=supervised_data2[:-12]
             test_data2=supervised_data2[-12:]
             
             scaler2=MinMaxScaler(feature_range=(-1,1))
             scaler2.fit(train_data2)
             train_data2=scaler2.transform(train_data2)
             test_data2=scaler2.transform(test_data2)
             
             x_train2,y_train2=train_data2[:,1:],train_data2[:,0:1]
             x_test2,y_test2=test_data2[:,1:],test_data2[:,0:1]
             y_train2=y_train2.ravel()
             y_test2=y_test2.ravel()
              #make prediction data frame
             sales_dates2=monthly_sales2['date'][-12:].reset_index(drop=True)
             predict_df2=pd.DataFrame(sales_dates2)
             act_sales2=monthly_sales2['sales'][-13:].to_list()
              #creat linear regression model and predicted output
             lr_model2=LinearRegression()
             lr_model2.fit(x_train2,y_train2)
             lr_pre2=lr_model2.predict(x_test2)
             
             lr_pre2=lr_pre2.reshape(-1,1)
              #matrix contains the output of the predicted data and test data input
             lr_pre_test_set2=np.concatenate([lr_pre2,x_test2],axis=1)
             lr_pre_test_set2=scaler2.inverse_transform(lr_pre_test_set2)
             
             result_list2=[]
             for index in range(0,len(lr_pre_test_set2)):
                  result_list2.append(lr_pre_test_set2[index][0]+act_sales2[index])
             lr_pre_series2=pd.Series(result_list2,name='linear prediction')
             predict_df2=predict_df2.merge(lr_pre_series2,left_index=True,right_index=True)
             #Erorrs of prediction
             answer2=input("if you want to display errors of prediction press \"y\" if you don't press anything else: ")
             if answer2=="y":
              lr_mse2=np.sqrt(mean_squared_error(predict_df2['linear prediction'],monthly_sales2['sales'][-12:]))
              lr_mae2=mean_absolute_error(predict_df2['linear prediction'],monthly_sales2['sales'][-12:])
              lr_r2_2=r2_score(predict_df2['linear prediction'],monthly_sales2['sales'][-12:])
              print("Linear regression MSE:  ",lr_mse2)
              print("linear regression MAE: ", lr_mae2)
              print("linear regression R2: ",lr_r2_2 )
             answer_of_graph2=input("If you want to display the graph press \"y\" if you don't press anything else: ") 
             if answer_of_graph2=="y":
                 plt.figure(figsize=(15,5))
                 #actual sales
                 plt.plot(monthly_sales2['date'],monthly_sales2['sales'])
                 #predicted sales
                 plt.plot(predict_df2['date'],predict_df2['linear prediction'])
                 plt.xlabel('Date')
                 plt.ylabel('Sales')
                 plt.title('Sales forcasting')
                 plt.legend(["Actual sales","Predicted sales"])
                 plt.show()
           
        elif(choice=='3'):
                 supervised_data3=monthly_sales3.drop(['date','sales'],axis=1)
                 for i3 in range(1,13):
                     col_name3='month_'+str(i3)
                     supervised_data3[col_name3]=supervised_data3['sales diff'].shift(i3)
                 supervised_data3=supervised_data3.dropna().reset_index(drop=True)
                 #split the data into train and test
                 train_data3=supervised_data3[:-12]
                 test_data3=supervised_data3[-12:]
                 
                 scaler3=MinMaxScaler(feature_range=(-1,1))
                 scaler3.fit(train_data3)
                 train_data3=scaler3.transform(train_data3)
                 test_data3=scaler3.transform(test_data3)
                 
                 x_train3,y_train3=train_data3[:,1:],train_data3[:,0:1]
                 x_test3,y_test3=test_data3[:,1:],test_data3[:,0:1]
                 y_train3=y_train3.ravel()
                 y_test3=y_test3.ravel()
                  #make prediction data frame
                 sales_dates3=monthly_sales3['date'][-12:].reset_index(drop=True)
                 predict_df3=pd.DataFrame(sales_dates3)
                 act_sales3=monthly_sales3['sales'][-13:].to_list()
                  #creat linear regression model and predicted output
                 lr_model3=LinearRegression()
                 lr_model3.fit(x_train3,y_train3)
                 lr_pre3=lr_model3.predict(x_test3)
                 
                 lr_pre3=lr_pre3.reshape(-1,1)
                  #matrix contains the output of the predicted data and test data input
                 lr_pre_test_set3=np.concatenate([lr_pre3,x_test3],axis=1)
                 lr_pre_test_set3=scaler3.inverse_transform(lr_pre_test_set3)
                 
                 result_list3=[]
                 for index in range(0,len(lr_pre_test_set3)):
                      result_list3.append(lr_pre_test_set3[index][0]+act_sales3[index])
                 lr_pre_series3=pd.Series(result_list3,name='linear prediction')
                 predict_df3=predict_df3.merge(lr_pre_series3,left_index=True,right_index=True)
                 #Erorrs of prediction
                 answer3=input("if you want to display errors of prediction press \"y\" if you don't press anything else: ")
                 if answer3=="y":
                  lr_mse3=np.sqrt(mean_squared_error(predict_df3['linear prediction'],monthly_sales3['sales'][-12:]))
                  lr_mae3=mean_absolute_error(predict_df3['linear prediction'],monthly_sales3['sales'][-12:])
                  lr_r2_3=r2_score(predict_df3['linear prediction'],monthly_sales3['sales'][-12:])
                  print("Linear regression MSE:  ",lr_mse3)
                  print("linear regression MAE: ", lr_mae3)
                  print("linear regression R2: ",lr_r2_3 )
                 answer_of_graph3=input("If you want to display the graph press \"y\" if you don't press anything else: ") 
                 if answer_of_graph3=="y":
                     plt.figure(figsize=(15,5))
                     #actual sales
                     plt.plot(monthly_sales3['date'],monthly_sales3['sales'])
                     #predicted sales
                     plt.plot(predict_df3['date'],predict_df3['linear prediction'])
                     plt.xlabel('Date')
                     plt.ylabel('Sales')
                     plt.title('Sales forcasting')
                     plt.legend(["Actual sales","Predicted sales"])
                     plt.show()
           

        else:
              print("unexpected value")
              predict_sales()
