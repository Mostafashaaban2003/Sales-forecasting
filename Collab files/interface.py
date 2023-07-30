
import user

passowrd1 = "142003"
password2 = "1234"
def system_init():
    mode = int(input("Please enter your mode:-"
                 "\n1. Who has the authority to display, remove and add"
                 "\n2. Who has the authority only to display\n"))
    while(not(mode < 3 and mode > 0)):
        mode = int(input("Invalid choice!"
                   "\nPlease enter number between 1~2: "))
    if(mode == 1):
        user.data_management.check_password(passowrd1)
        print("Choose any of these privileges:\n"
              "1. Display store sales\n"
              "2. Display all sales\n"
              "3. Display monthly sales\n"
              "4. Display upcoming sales forecast\n"
              "5. Edit password\n"
              "6. Add or Edit sales record\n"
              "7. Remove sales record\n"
              "8. Logout\n"
              "9. Exit\n")
        choice = user.data_management.choose_number(10)
        if (choice == 1):
            user.display_store_sales()
        elif (choice == 2):
            user.display_all_sales()
        elif (choice == 3):
            user.display_monthly_sales()
        elif(choice == 4):
            user.predict_sales()
        elif (choice == 5):
            user.edit_password()
        elif (choice == 6):
            user.add_or_edit_sales_record()
        elif (choice == 7):
            user.remove_sales_record()
        elif (choice == 8):
            system_init()
        elif (choice == 9):
            exit()
    else:
        user.data_management.check_password(password2)
        print("Choose any of these privileges:\n"
              "1. Display sales record\n"
              "2. Display all sales\n"
              "3. Display monthly sales\n"
              "4. Display upcoming sales forecast\n"
              "5. Edit password\n"
              "6. Logout\n"
              "7. Exit\n")
        choice = user.data_management.choose_number(7)
        if (choice == 1):
            user.display_store_sales()
        elif (choice == 2):
            user.display_all_sales()
        elif (choice == 3):
            user.display_monthly_sales()
        elif(choice == 4):
            user.predict_sales()
        elif (choice == 5):
            user.edit_password()
        elif (choice == 6):
            system_init()
        elif (choice == 7):
            exit()


system_init()



