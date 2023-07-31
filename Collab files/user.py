import data_management
# function to display stationary data for user
def display_store_sales():
    branch_sales = data_management.branch_selection()
    choice = input("Enter 1 for \"Year\" or 2 for \"Month\" or anything else for \"Day\": ")
    # while(True) to get valid data
    while (True):
        year = int(input("Enter the year: "))
        if (year >= 2013):
            constant = int((year - 2012) / 4)
            break

    if (choice == '1'):
        year_sales = branch_sales.loc[(year - 2013) * 365 + constant - bool(year % 4 == 0): (year + 1 - 2013) * 365 + constant - 1]
        print(year_sales)
        data_management.do_you_want_to_display_a_graph(year_sales, 100, 5)

    elif (choice == '2'):
        while (True):
            month = int(input("Enter the month: "))
            if (month > 12 or month <= 0):
                continue
            else:
                month_sales = branch_sales.loc[(year - 2013) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0): (year - 2013) * 365 + constant - 1 + abs((2 - month)) * 30 + bool(not (month <= 2)) * (month - bool(month < 8)) / 2 + bool(month <= 2) * (58 + bool(year % 4 == 0)) * abs(month - 1) + bool((not (month <= 2))) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0)]
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
            index_day = int((year - 2013) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0) - 1 + day)
            print(branch_sales.loc[index_day])
            break

def display_all_sales():
    branch_sales = data_management.branch_selection()
    print(branch_sales)
    data_management.do_you_want_to_display_a_graph(branch_sales, 50, 10)
    return
def display_monthly_sales():
    branch_sales = data_management.branch_selection()
    choice = input("Enter 1 for \"Year\" or anything else for \"Month\": ")
    while(True):
        year = int(input("Which year?\n"))
        if(year > 2012):
            break
    if(choice == '1'):
        print(data_management.to_monthly_sales(branch_sales, 0).loc[(year - 2013) * 12: (year - 2013) * 12 + 11])
    else:
        while(True):
            month = int(input("Which month?\n"))
            if(month > 0 and month <= 12):
                print(data_management.to_monthly_sales(branch_sales, 0).loc[(year - 2013) * 12 + month - 1])
                break

# to predict sales
def predict_sales():
    branch_sales = data_management.branch_selection()
    month_sales = data_management.to_monthly_sales(branch_sales , 1)
    supervised_data = month_sales.drop(['date', 'sales'], axis=1)
    for i in range(1, 13):
        col_name = 'month_' + str(i)
        supervised_data[col_name] = supervised_data['sales diff'].shift(i)
    supervised_data = supervised_data.dropna().reset_index(drop=True)
        # split the data into train and test
    train_data = supervised_data[:-94]
    test_data = supervised_data[-12:]

    scaler = data_management.MinMaxScaler(feature_range=(-1, 1))
    scaler.fit(train_data)
    train_data = scaler.transform(train_data)
    test_data = scaler.transform(test_data)

    x_train, y_train = train_data[:, 1:], train_data[:, 0:1]
    x_test, y_test = test_data[:, 1:], test_data[:, 0:1]
    y_train = y_train.ravel()
    y_test = y_test.ravel()
    # make prediction data frame
    sales_dates = month_sales['date'][-12:].reset_index(drop=True)
    predict_df = data_management.pd.DataFrame(sales_dates)
    act_sales = month_sales['sales'][-24:].to_list()
    # creat linear regression model and predicted output
    lr_model = data_management.LinearRegression()
    lr_model.fit(x_train, y_train)
    lr_pre = lr_model.predict(x_test)
    lr_pre = lr_pre.reshape(-1, 1)
    # matrix contains the output of the predicted data and test data input
    lr_pre_test_set = data_management.np.concatenate([lr_pre, x_test], axis=1)
    lr_pre_test_set = scaler.inverse_transform(lr_pre_test_set)

    result_list = []
    for index in range(0, len(lr_pre_test_set)):
        result_list.append(lr_pre_test_set[index][0] + act_sales[index])
    lr_pre_series = data_management.pd.Series(result_list, name='linear prediction')
    predict_df = predict_df.merge(lr_pre_series, left_index=True, right_index=True)
    # Erorrs of prediction
    answer = input("if you want to display errors of prediction press \"y\" if you don't press anything else: ")
    if answer == "y":
            lr_mse = data_management.np.sqrt(data_management.mean_squared_error(predict_df['linear prediction'], month_sales['sales'][-12:]))
            lr_mae = data_management.mean_absolute_error(predict_df['linear prediction'], month_sales['sales'][-12:])
            lr_r2 = data_management.r2_score(predict_df['linear prediction'], month_sales['sales'][-12:])
            print("Linear regression MSE:  ", lr_mse)
            print("Linear regression MAE: ", lr_mae)
            print("Linear regression R2: ", lr_r2)
    answer_of_graph = input("If you want to display the graph press \"y\" if you don't press anything else: ")
    if answer_of_graph == "y":
        data_management.plt.figure(figsize=(15, 5))
        # actual sales
        data_management.plt.plot(month_sales['date'][:-12], month_sales['sales'][:-12])
        # predicted sales
        data_management.plt.plot(predict_df['date'], predict_df['linear prediction'])
        data_management.plt.xlabel('Date')
        data_management.plt.ylabel('Sales')
        data_management.plt.title('Sales forcasting')
        data_management.plt.legend(["Actual sales", "Predicted sales"])
        data_management.plt.show()

def edit_password(password):
    old_password = input("Enter old password: ")
    i = 0
    while (old_password != password):
        print("INVALID PASSWORD.\n"
        "You Have", 9 - i, " More Tries.\n")
        old_password = input("Enter old password: ")
        i = i + 1
        if (i == 9):
            exit()
        new_password = input("Enter new password: ")
        old_password = new_password
        print("\nPassword Changed Successfully!")
def add_or_edit_sales_record():
    branch_sales = data_management.branch_selection_for_files()
    while (True):
        year = int(input("Enter the year: "))
        if (year >= 2013):
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
    df = data_management.pd.read_csv(branch_sales)
    # updating the column value/data
    df.loc[(year - 2013) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0) - 1 + day , 'sales'] = sales

    # writing into the file
    df.to_csv(branch_sales, index=False)

    print("\nData Added Successfully!\n")
    more_data = input("Do You Want To Add More Data?"
                      "Enter \'Y\' For \"Yes\" And Anything Else For \"No\": ")
    if(more_data == 'Y' or more_data == 'y'):
        add_or_edit_sales_record()

def remove_sales_record():
    branch_sales = data_management.branch_selection_for_files()
    choice = input("Enter 1 for \"Year\" or 2 for \"Month\" or anything else for \"Day\": ")
    while (True):
        year = int(input("Enter the year: "))
        if (year >= 2013):
            constant = int((year - 2012) / 4)
            break
    df = data_management.pd.read_csv(branch_sales)
    if (choice == '1'):
        df.loc[(year - 2013) * 365 + constant - bool(year % 4 == 0): (year + 1 - 2013) * 365 + constant - 1, 'sales'] = '\0'
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
        df.loc[(year - 2013) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0): (year - 2013) * 365 + constant - 1 + abs((2 - month)) * 30 + bool(not (month <= 2)) * (month - bool(month < 8)) / 2 + bool(month <= 2) * (58 + bool(year % 4 == 0)) * abs(month - 1) + bool((not (month <= 2))) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0), 'sales'] = '\0'
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
        df.loc[(year - 2013) * 365 + constant - 1 + (month - 1 - 2 * bool(not (month <= 2))) * (30 + bool(month <= 2)) + bool(not (month <= 2)) * ((month - 1 - bool(month < 8)) / 2) + bool(not (month <= 2)) * ((month - bool(month < 8)) % 2) + bool(not (month <= 2)) * (58 + bool(year % 4 == 0)) + bool(year % 4 != 0) - 1 + day, 'sales'] = '\0'
        df.to_csv(branch_sales, index=False)
        print("Data For This Day Removed Successfully!")
        more_data = input("Do You Want To Remove More Data?"
                          "Enter \'Y\' For \"Yes\" And Anything Else For \"No\": ")
        if (more_data == 'Y' or more_data == 'y'):
            remove_sales_record()
        return
    
