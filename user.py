import pandas as pd

import data_management
import xlsxwriter
import csv
import datetime

#monthly_sales1['date'] = ['date'].dt.to_timestamp()
# function to display stationary data for user
def display_store_sales():
    branch_sales = data_management.branch_selection()
    choice = input("Enter 1 for \"Year\" or 2 for \"Month\" or anything else for \"Day\": ")
    # while(True) to get valid data
    while (True):
        year = int(input("Enter the year: "))
        if (year >= data_management.start_day):
            constant = int((year - 2012) / 4)
            break

    if (choice == '1'):
        year_sales = branch_sales.loc[(year - data_management.start_day) * 365 + constant - bool(year % 4 == 0): (year + 1 - data_management.start_day) * 365 + constant - 1]
        print(year_sales)
        data_management.do_you_want_to_display_a_graph(year_sales, 450, 5)

    elif (choice == '2'):
        while (True):
            month = int(input("Enter the month: "))
            if (month > 12 or month <= 0):
                continue
            else:
                month_sales = branch_sales.loc[(year - data_management.start_day) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0): (year - data_management.start_day) * 365 + constant - 1 + abs((2 - month)) * 30 + bool(not (month <= 2)) * (month - bool(month < 8)) / 2 + bool(month <= 2) * (58 + bool(year % 4 == 0)) * abs(month - 1) + bool((not (month <= 2))) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0)]
                print(month_sales)
                data_management.do_you_want_to_display_a_graph(month_sales, 40, 10)
                break

    else:
        while (True):
            month = int(input("Enter the month: "))
            if (month <= 12 and month > 0):
                break
        while (True):
            day = int(input("Enter the day: "))
            if ((day > 31 or day <= 0) or (day == 31 and (month == 4 or month == 6 or month == 9 or month == 11)) or (day > 28 and month == 2 and year % 4 != 0) or (day > 29 and month == 2 and year % 4 == 0)):
                continue
            index_day = int((year - data_management.start_day) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0) - 1 + day)
            print(branch_sales.loc[index_day])
            break

def display_all_sales():
    branch_sales = data_management.branch_selection()
    print(branch_sales)
    data_management.do_you_want_to_display_a_graph(branch_sales, 50, 10)

    return





# to display monthly sales and monthly sales difference
def to_monthly_sales(num_branch_sales):
    # converting date to a Month period
    monthly_sales = num_branch_sales
    monthly_sales['date'] = monthly_sales['date'].dt.to_period("M")
    # sum the number of items in each month
    monthly_sales = monthly_sales.groupby('date').sum().reset_index()
    # convert date to timestamp datatype
    sales_different = input("Do you want to display sales different between each month and the one before it ?"
                            "\nEnter 1 for \"Yes\" and anything else for \"No\": ")
    if(sales_different == '1'):
        monthly_sales['sales diff'] = monthly_sales['sales'].diff()

    # delete the rows with missing values
    monthly_sales = monthly_sales.dropna()
    return monthly_sales




def display_monthly_sales():
    branch_sales = data_management.branch_selection()
    choice = input("Enter 1 for \"Year\" or anything else for \"Month\": ")
    while(True):
        year = int(input("Which year?\n"))
        if(year > 2012):
            break
    if(choice == '1'):
        print(print(to_monthly_sales(branch_sales).loc[(year - data_management.start_day) * 12: (year - data_management.start_day) * 12 + 11]))

    else:
        while(True):
            month = int(input("Which month?\n"))
            if(month > 0 and month <= 12):
                print(to_monthly_sales(branch_sales).loc[(year - data_management.start_day) * 12 + month - 1])
                break

#display_store_sales()


def add_or_edit_sales_record():
    branch_sales = data_management.branch_selection_for_files()
    while (True):
        year = int(input("Enter the year: "))
        if (year >= data_management.start_day):
            constant = int((year - 2012) / 4)
            break
    while (True):
        month = int(input("Enter the month: "))
        if (month <= 12 and month > 0):
            break
    while (True):
        day = int(input("Enter the day: "))
        if ((day > 31 or day <= 0) or (day == 31 and (month == 4 or month == 6 or month == 9 or month == 11)) or (day > 28 and month == 2 and year % 4 != 0) or (day > 29 and month == 2 and year % 4 == 0)):
            continue
        break
    sales = input("Enter the sales: ")
    df = pd.read_csv(branch_sales)
    # updating the column value/data
    df.loc[(year - data_management.start_day) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0) - 1 + day , 'sales'] = sales

    # writing into the file
    df.to_csv(branch_sales)

    print("Data Added Successfully!")
    more_data = input("Do You Want To Add More Students?"
                      "Enter \'Y\' For \"Yes\" And Anything Else For \"No\": ")
    if(more_data == 'Y' or more_data == 'y'):
        add_or_edit_sales_record()

def remove_sales_record():
    branch_sales = data_management.branch_selection_for_files()
    choice = input("Enter 1 for \"Year\" or 2 for \"Month\" or anything else for \"Day\": ")
    while (True):
        year = int(input("Enter the year: "))
        if (year >= data_management.start_day):
            constant = int((year - 2012) / 4)
            break
    df = pd.read_csv(branch_sales)
    if (choice == '1'):
        df.loc[(year - data_management.start_day) * 365 + constant - bool(year % 4 == 0): (year + 1 - data_management.start_day) * 365 + constant - 1, 'sales'] = '\0'
        df.to_csv(branch_sales, index=False)
        print("Data For This Year Removed Successfully!")
        more_data = input("Do You Want To Remove More Data?"
                          "Enter \'Y\' For \"Yes\" And Anything Else For \"No\": ")
        if (more_data == 'Y' or more_data == 'y'):
            add_or_edit_sales_record()
        return

    elif(choice == '2'):
        while (True):
            month = int(input("Enter the month: "))
            if (month <= 12 and month > 0):
                break
        df.loc[(year - data_management.start_day) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0): (year - data_management.start_day) * 365 + constant - 1 + abs((2 - month)) * 30 + bool(not (month <= 2)) * (month - bool(month < 8)) / 2 + bool(month <= 2) * (58 + bool(year % 4 == 0)) * abs(month - 1) + bool((not (month <= 2))) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0), 'sales'] = '\0'
        df.to_csv(branch_sales, index=False)
        print("Data For This Month Removed Successfully!")
        more_data = input("Do You Want To Remove More Data?"
                          "Enter \'Y\' For \"Yes\" And Anything Else For \"No\": ")
        if (more_data == 'Y' or more_data == 'y'):
            remove_sales_record()
        return
    else:
        while (True):
            month = int(input("Enter the month: "))
            if (month <= 12 and month > 0):
                break
        while (True):
            day = int(input("Enter the day: "))
            if ((day > 31 or day <= 0) or (day == 31 and (month == 4 or month == 6 or month == 9 or month == 11)) or (day > 28 and month == 2 and year % 4 != 0) or (day > 29 and month == 2 and year % 4 == 0)):
                continue
            break
        df.loc[(year - data_management.start_day) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0) - 1 + day, 'sales'] = '\0'
        df.to_csv(branch_sales, index=False)
        print("Data For This Day Removed Successfully!")
        more_data = input("Do You Want To Remove More Data?"
                          "Enter \'Y\' For \"Yes\" And Anything Else For \"No\": ")
        if (more_data == 'Y' or more_data == 'y'):
            remove_sales_record()
        return

def edit_password(password):
    old_password = input("Enter old password: ")
    i = 0
    while (old_password != password):
        print("INVALID PASSWORD.\n"
          "You Have", 9 - i, " More Tries.\n")
        old_password = input("Enter your password: ")
        i = i + 1
        if (i == 9):
            exit()
    new_password = input("Enter new password: ")
    old_password = new_password
    print("\nPassword Changed Successfully!")
