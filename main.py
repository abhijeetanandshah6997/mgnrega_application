# main function
import os
import sqlite3
from sqlite3 import Error
from getpass import getpass

from controllers.login import Login
from models.user import User


def db_connection():
    """ create a database connection to the SQLite database
    :return: Connection object or None
    """
    try:
        con = sqlite3.connect('mgnrega.sqlite')
        return con
    except Error:
        print(Error)


def new_account():
    print('\n')
    username = input('Enter username : ')
    password = input('Enter password : ')
    email = input('Enter email : ')
    first_name = input('Enter first name : ')
    last_name = input('Enter last name : ')
    age = int(input('Enter age : '))
    gender = input('Enter gender (M/F) : ')
    contact = input('Enter contact : ')
    area = input('Enter Area - District,State : ')
    pin_code = input('Enter pin code : ')
    role = input('Enter role (gpm/member) : ')
    new_user = User(username, password, email, first_name, last_name, age, gender, contact, area, pin_code, role)
    return new_user


def user_list(users):
    print('\nSr. No.\t\tUser ID\t\tUsername\t\tRole')
    for idx, user in enumerate(users, start=1):
        print(str(idx) + "\t\t" + str(user['user_id']) + "\t\t" + user['username'] + "\t\t\t" + user['role'])


def main():
    os.system('clear')
    conn = db_connection()
    conn.row_factory = sqlite3.Row
    while True:
        print("\nWelcome to MGNREGA Application :- \n(1)Login\n(2)Quit\n")
        ch = input(">> ").lower().rstrip()
        if ch == "1":
            os.system('clear')
            print("\nLogin to MGNREGA Application\n")
            username = input('Username : ')
            password = getpass('Password : ')
            with conn:
                login_user = Login.login(conn, username=username, password=password)
                if login_user is not None:
                    if login_user['role'] == 'bdo':
                        while True:
                            os.system('clear')
                            print(login_user)
                            print(f"Welcome ! {login_user['first_name']}...")

                            print("\nMenu"
                                  "\n(1)Add New GPM Account"
                                  "\n(2)Show Reporting GPM Accounts"
                                  "\n(3)Update GPM Account"
                                  "\n(4)Delete GPM Account"
                                  "\n(5)Logout\n")
                            ch = input(">> ").lower().rstrip()
                            if ch == "1":
                                new_user_details = new_account()
                                new_users_id = new_user_details.add_user(conn)
                                if new_users_id is not None:
                                    print(new_users_id)
                                conn.commit()
                                input("\nPress Enter to continue...")
                            elif ch == "2":
                                users = User.view_specific_users(conn)
                                if users is not None:
                                    user_list(users)
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "3":
                                users = User.view_specific_users(conn)
                                if users is not None:
                                    user_list(users)
                                    user_to_be_updated = input("\nEnter username to be updated : ").lower().rstrip()
                                    print("\nSelect Field/(s) to Update:-"
                                          "\n username"
                                          "\n password"
                                          "\n email"
                                          "\n first_name"
                                          "\n last_name"
                                          "\n age"
                                          "\n gender"
                                          "\n contact"
                                          "\n area"
                                          "\n pin_code"
                                          "\n role"
                                          "\n is_deleted"
                                          "\n")
                                    fields = ["username", "password", "email", "first_name", "last_name", "age",
                                              "gender", "contact", "area", "pin_code", "role", "is_deleted", ]
                                    field_to_update = dict()
                                    more = 'y'
                                    while more == 'y':
                                        field_name = input("Enter field name : ").lower().rstrip()
                                        if field_name in fields:
                                            field_value = input("Enter field value : ")
                                            field_to_update[field_name] = field_value
                                            more = input("Update more Fields (Y/N) : ").lower().rstrip()
                                        else:
                                            print("\n No such field.. Please try again...")
                                            more = 'y'
                                    updated_user = User.update_user(conn, user_to_be_updated, **field_to_update)
                                    if updated_user is 0:
                                        print("User is doesn't exists")
                                    else:
                                        print(f"User {user_to_be_updated} is updated.")
                                    conn.commit()
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "4":
                                users = User.view_specific_users(conn)
                                if users is not None:
                                    user_list(users)
                                    user_to_be_deleted = input("\nEnter username to be deleted : ").lower().rstrip()
                                    deleted_user = User.delete_user(conn, user_to_be_deleted)
                                    if deleted_user is 0:
                                        print("User is doesn't exists")
                                    else:
                                        print(f"User {user_to_be_deleted} is deleted.")
                                    conn.commit()
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "5":
                                Login.logged_in_user = dict()
                                os.system('clear')
                                break
                            else:
                                print("Invalid choice, please choose again\n")
                    elif login_user['role'] == 'gpm':
                        while True:
                            os.system('clear')
                            print(login_user)
                            print(f"Welcome ! {login_user['first_name']}...")
                            print("\nMenu\n(1)Something\n(2)Something Else\n(3)Logout\n")
                            ch = input(">> ").lower().rstrip()
                            if ch == "1":
                                pass
                            elif ch == "2":
                                pass
                            elif ch == "3":
                                Login.logged_in_user = dict()
                                os.system('clear')
                                break
                            else:
                                print("Invalid choice, please choose again\n")
                    elif login_user['role'] == 'member':
                        while True:
                            os.system('clear')
                            print(login_user)
                            print(f"Welcome ! {login_user['first_name']}...")
                            print("\nMenu\n(1)Something\n(2)Something Else\n(3)Logout\n")
                            ch = input(">> ").lower().rstrip()
                            if ch == "1":
                                pass
                            elif ch == "2":
                                pass
                            elif ch == "3":
                                Login.logged_in_user = dict()
                                os.system('clear')
                                break
                            else:
                                print("Invalid choice, please choose again\n")
                    else:
                        print('Not a valid user..!!!')
                else:
                    print('No user found... Try Login Again...')
        elif ch == "2":
            os.system('clear')
            break
        else:
            print("Invalid choice, please choose again\n")


if __name__ == '__main__':
    main()
