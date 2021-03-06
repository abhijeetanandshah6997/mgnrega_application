import os
import re
import sqlite3
from sqlite3 import Error
from getpass import getpass
from datetime import datetime

from controllers.login import Login
from models.complaints import Complaints
from models.user import User
from models.project import Project
from models.user_project_wage import UserProjectWage


class DataBaseClass:

    @staticmethod
    def db_connection():
        """ create a database connection to the SQLite database
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect('mgnrega.sqlite')
            return conn
        except Error:
            print(Error)


def int_input(input_message):
    try:
        int_val = int(input(input_message))
        return int_val
    except:
        print("Wrong Input.. Try Again...")
        return None


regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def email_input():
    email = input('Enter email : ')
    if re.search(regex, email):
        return email
    else:
        print("Wrong Input.. Try Again...")
        return None


re_gender = ['M', 'F']


def gender_input():
    gender = input('Enter gender (M/F) : ').upper()
    if gender in re_gender:
        return gender
    else:
        print("Wrong Input.. Try Again...")
        return None


re_role = ['gpm', 'member']


def role_input():
    role = input('Enter role (gpm/member) : ').lower()
    if role in re_role:
        return role
    else:
        print("Wrong Input.. Try Again...")
        return None


def new_account():
    """
    Take inputs from user and create an instance of User Class
    :return: User object
    """
    print('\n')
    username = input('Enter username : ')
    password = input('Enter password : ')
    email = None
    while email is None:
        email = email_input()
    first_name = input('Enter first name : ')
    last_name = input('Enter last name : ')
    age = None
    while age is None:
        age = int_input('Enter age : ')
    gender = None
    while gender is None:
        gender = gender_input()
    contact = None
    while contact is None:
        contact = int_input('Enter contact : ')
    area = input('Enter Area - District,State : ')
    pin_code = None
    while pin_code is None:
        pin_code = int_input('Enter pin code : ')
    role = None
    while role is None:
        role = role_input()
    new_user = User(username, password, email, first_name, last_name, age, gender, contact, area, pin_code, role)
    return new_user


def new_project():
    """
    Take inputs from user for creating a new project instance of Project Class
    :return: Project Object
    """
    print('\n')
    project_name = input('Enter Project name : ')
    project_type = input('Enter Project type (Road Construction/Sewage Treatment/ Building Construction) : ')
    area = input('Enter Area : ')
    total_required_member = None
    while total_required_member is None:
        total_required_member = int_input('Enter total no. of required Members : ')
    cost_estimate = float(input('Enter cost estimate : '))
    start_date = datetime.strptime(input('Enter start date (YYYY-MM-DD) : '), '%Y-%m-%d').date()
    end_date_estimate = datetime.strptime(input('Enter end date estimate (YYYY-MM-DD) : '), '%Y-%m-%d').date()
    new_project_obj = Project(project_name, project_type, area, total_required_member, cost_estimate, start_date, end_date_estimate)
    return new_project_obj


def new_project_assignment():
    """
    Take inputs from user to associate a project with member and create an instance of UserProjectWage Class
    :return: UserProjectWage Object
    """
    print('\n')
    user_id = None
    while user_id is None:
        user_id = int_input('Enter user_id to be assigned a project : ')
    project_id = None
    while project_id is None:
        project_id = int_input('Enter project_id user will be assigned : ')
    no_of_days_worked = None
    while no_of_days_worked is None:
        no_of_days_worked = int_input('Enter number of days worked: ')
    wage = no_of_days_worked * 100.0
    attendance = None
    while attendance is None:
        attendance = int_input('Enter attendance: ')
    new_user_project_wage = UserProjectWage(user_id, project_id, no_of_days_worked, wage, attendance)
    return new_user_project_wage


def new_complaint(bdo_user_id, gpm_user_id):
    """
    Take input from user to file complaints and create an instance Complaints Class
    :return: Complaints Object
    """
    print('\n')
    user_id = Login.logged_in_user['user_id']
    complaint_subject = input('Enter Complaint Subject : ')
    complaint_description = input('Enter Complaint Description : ')
    new_user_complaint = Complaints(user_id, bdo_user_id, gpm_user_id, complaint_subject, complaint_description)
    return new_user_complaint


def user_list(users):
    """
    Function that take a list of users and prints in a particular specified format.
    :param users: a list of users details
    """
    print('\nSr. No.\t\tUser ID\t\tUsername\t\tRole')
    for idx, user in enumerate(users, start=1):
        print(str(idx) + "\t\t" + str(user['user_id']) + "\t\t" + user['username'] + "\t\t\t" + user['role'])


def project_list(projects):
    """
    Function that take a list of projects and prints in a particular specified format.
    :param projects: a list of project details
    """
    print('\nSr. No.\tProject ID\tProject Name\t\tProject Type\t\tArea\t\tRequired Members\tCost Estimate\t\tStart Date\tEnd Date Estimate')
    for idx, project in enumerate(projects, start=1):
        print(str(idx) + "\t" + str(project['project_id']) + "\t\t" + project['project_name'] + "\t" + project['project_type'] + "\t" + project['area'] + "\t" + str(project['total_required_member']) + "\t\t\tRs. " + str(project['cost_estimate']) + "\t" + project['start_date'] + "\t" + project['end_date_estimate'])


def user_project_list(conn, user_projects):
    """
    Function that take a list of user association with projects and prints in a particular specified format.
    :param conn: a sqlite db connection object
    :param user_projects: a list of user project association
    """
    print('\nSr. No.\tUser ID\tUsername\tProject ID\tProject Name\t\tDays Worked\tWage\t\t\tAttendance\tBDO Approved\tWage Approved\tJob Card Issued')
    for idx, user_project in enumerate(user_projects, start=1):
        user = User.view_user_details(conn, user_project['user_id'])
        project = Project.view_project_details(conn, user_project['project_id'])
        print(str(idx) + "\t" + str(user['user_id']) + "\t" + str(user['username']) + "\t\t" + str(project['project_id']) + "\t\t" + str(project['project_name']) + "\t" + str(user_project['no_of_days_worked']) + "\t\tRs. " + str(user_project['wage']) + "\t\t" + str(user_project['attendance']) + "\t\t" + approval_status(user_project['is_bdo_approved']) + "\t\t" + approval_status(user_project['is_wage_approved']) + "\t\t" + approval_status(user_project['is_job_card_issued']))


def complaint_list(complaints):
    """
    Function that take a list of complaints and prints in a particular specified format.
    :param complaints: a list of filed complaints by the user
    """
    print('\nSr. No.\tUser ID\tBDO ID\tGPM ID\tComplain Subject\tComplain Description\t\t\t\tComplain Date\tResolved')
    for idx, complaint in enumerate(complaints, start=1):
        print(str(idx) + "\t" + str(complaint['user_id']) + "\t" + str(complaint['bdo_user_id']) + "\t" + str(complaint['gpm_user_id']) + "\t" + complaint['complain_subject'] + "\t\t" + str(complaint['complain_description'])[:20] + "...\t\t\t\t" + str(datetime.strptime(complaint['created_at'], '%Y-%m-%d %H:%M:%S.%f').date()) + "\t" + approval_status(complaint['is_resolved']))


def approval_status(value):
    """
    Function that return string value for boolean
    :param value: a boolean value
    :return: corresponding string -  YES for True (1) and NO for False (0)
    """
    if value:
        return 'YES'
    else:
        return 'NO'


def main():
    """
    Driver Function from where the program is executed and is responsible for providing the Menu Driven Approach for
    MGNREGA Application Features.
    """
    os.system('clear')
    conn = DataBaseClass.db_connection()    # Database Connection Object
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
                if login_user == 'access_denied':
                    print('Access Denied..!! Contact BDO.')
                elif login_user is not None:
                    if login_user['role'] == 'bdo':     # Checks if the Logged in user role is BDO
                        while True:
                            os.system('clear')
                            print(f"Welcome ! {login_user['first_name']}...")
                            print("\nMenu"
                                  "\n(1)Add New GPM/Member Account"
                                  "\n(2)View Reporting GPMs & corresponding Members"
                                  "\n(3)Update Account"
                                  "\n(4)Delete Account"
                                  "\n(5)Create Project"
                                  "\n(6)View Projects"
                                  "\n(7)Update Project"
                                  "\n(8)Delete Project"
                                  "\n(9)Approve Member Assignment"
                                  "\n(10)Approve Wage"
                                  "\n(11)Pending Approval Requests"
                                  "\n(12)See All Complaints"
                                  "\n(13)Logout\n")
                            ch = input(">> ").lower().rstrip()
                            if ch == "1":
                                new_user_details = new_account()
                                if new_user_details.role == 'member':
                                    users = User.view_specific_users(conn)
                                    if users is not None and users:
                                        users = [user for user in users if user['role'] == 'gpm']
                                        user_list(users)
                                        gpm_user_id = None
                                        while gpm_user_id is None:
                                            gpm_user_id = int_input('Enter GPM\'s user_id to be assigned the member : ')
                                        new_users_id = new_user_details.add_user(conn, gpm_user_id)
                                        if new_users_id is not None:
                                            print(new_users_id)
                                        conn.commit()
                                    else:
                                        print("No reporting user available...")
                                elif new_user_details.role == 'gpm':
                                    new_users_id = new_user_details.add_user(conn)
                                    if new_users_id is not None:
                                        print(new_users_id)
                                    conn.commit()
                                input("\nPress Enter to continue...")
                            elif ch == "2":
                                users = User.view_specific_users(conn)
                                if users is not None and users:
                                    user_list(users)
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "3":
                                users = User.view_specific_users(conn, action='update')
                                if users is not None and users:
                                    user_list(users)
                                    user_to_be_updated = input("\nEnter username to be updated : ").lower().rstrip()
                                    print("\nSelect Field/(s) to Update:-"
                                          "\n password"
                                          "\n email"
                                          "\n first_name"
                                          "\n last_name"
                                          "\n age"
                                          "\n gender"
                                          "\n contact"
                                          "\n area"
                                          "\n pin_code"
                                          "\n is_deleted"
                                          "\n")
                                    fields = ["password", "email", "first_name", "last_name", "age",
                                              "gender", "contact", "area", "pin_code", "is_deleted", ]
                                    field_to_update = dict()
                                    more = 'y'
                                    while more == 'y':
                                        field_name = input("Enter field name : ").lower().rstrip()
                                        field_value = None
                                        if field_name in fields:
                                            if field_name == 'is_deleted':
                                                incorrect_field_val = True
                                                while incorrect_field_val:
                                                    field_value = input("Enter field value (Y/N): ").lower().rstrip()
                                                    if field_value == 'y':
                                                        incorrect_field_val = False
                                                        field_value = 1
                                                    elif field_value == 'n':
                                                        incorrect_field_val = False
                                                        field_value = 0
                                                    else:
                                                        incorrect_field_val = True
                                                        print("Invalid Input... Try Again...")
                                            elif field_name == 'email':
                                                field_value = None
                                                while field_value is None:
                                                    field_value = email_input()
                                            elif field_name == 'age':
                                                field_value = None
                                                while field_value is None:
                                                    field_value = int_input("Enter Age : ")
                                            elif field_name == 'gender':
                                                field_value = None
                                                while field_value is None:
                                                    field_value = gender_input()
                                            elif field_name == 'contact':
                                                field_value = None
                                                while field_value is None:
                                                    field_value = int_input("Enter Contact No. : ")
                                            elif field_name == 'pin_code':
                                                field_value = None
                                                while field_value is None:
                                                    field_value = int_input("Enter Pin Code : ")
                                            else:
                                                field_value = input("Enter field value : ")
                                            field_to_update[field_name] = field_value
                                            more = input("Update more Fields (Y/N) : ").lower().rstrip()
                                        else:
                                            print("\n No such field.. Please try again...")
                                            more = 'y'
                                    updated_user = User.update_user(conn, user_to_be_updated, **field_to_update)
                                    if updated_user is 0:
                                        print("User doesn't exists")
                                    else:
                                        print(f"User {user_to_be_updated} is updated.")
                                    conn.commit()
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "4":
                                users = User.view_specific_users(conn)
                                if users is not None and users:
                                    user_list(users)
                                    user_to_be_deleted = input("\nEnter username to be deleted : ").lower().rstrip()
                                    deleted_user = User.delete_user(conn, user_to_be_deleted)
                                    if deleted_user is 0:
                                        print("User doesn't exists")
                                    else:
                                        print(f"User {user_to_be_deleted} is deleted.")
                                    conn.commit()
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "5":
                                new_project_details = new_project()
                                new_project_id = new_project_details.add_project(conn)
                                if new_project_id is not None:
                                    print(new_project_id)
                                conn.commit()
                                input("\nPress Enter to continue...")
                            elif ch == "6":
                                projects = Project.view_specific_projects(conn)
                                if projects:
                                    project_list(projects)
                                else:
                                    print("No projects available...")
                                input("\nPress Enter to continue...")
                            elif ch == "7":
                                projects = Project.view_specific_projects(conn, action='update')
                                if projects is not None:
                                    project_list(projects)
                                    project_id_to_be_updated = None
                                    while project_id_to_be_updated is None:
                                        project_id_to_be_updated = int_input("\nEnter project_id to be updated : ")
                                    print("\nSelect Field/(s) to Update:-"
                                          "\n project_name"
                                          "\n project_type"
                                          "\n area"
                                          "\n total_required_member"
                                          "\n cost_estimate"
                                          "\n start_date"
                                          "\n end_date_estimate"
                                          "\n is_deleted"
                                          "\n")
                                    fields = ["project_name", "project_type", "area", "total_required_member", "cost_estimate", "start_date", "end_date_estimate", "is_deleted", ]
                                    field_to_update = dict()
                                    more = 'y'
                                    while more == 'y':
                                        field_name = input("Enter field name : ").lower().rstrip()
                                        if field_name in fields:
                                            if field_name == 'is_deleted':
                                                incorrect_field_val = True
                                                while incorrect_field_val:
                                                    field_value = input("Enter field value (Y/N): ").lower().rstrip()
                                                    if field_value == 'y':
                                                        incorrect_field_val = False
                                                        field_value = 1
                                                    elif field_value == 'n':
                                                        incorrect_field_val = False
                                                        field_value = 0
                                                    else:
                                                        incorrect_field_val = True
                                                        print("Invalid Input... Try Again...")
                                            else:
                                                field_value = input("Enter field value : ")
                                            field_to_update[field_name] = field_value
                                            more = input("Update more Fields (Y/N) : ").lower().rstrip()
                                        else:
                                            print("\n No such field.. Please try again...")
                                            more = 'y'
                                    updated_project = Project.update_project(conn, project_id_to_be_updated, **field_to_update)
                                    if updated_project is 0:
                                        print("Project doesn't exists")
                                    else:
                                        print(f"Project {project_id_to_be_updated} is updated.")
                                    conn.commit()
                                else:
                                    print("No projects available...")
                                input("\nPress Enter to continue...")
                            elif ch == "8":
                                projects = Project.view_specific_projects(conn)
                                if projects:
                                    project_list(projects)
                                    project_id_to_be_deleted = None
                                    while project_id_to_be_deleted is None:
                                        project_id_to_be_deleted = int_input("\nEnter project_id to be deleted : ")
                                    deleted_project = Project.delete_project(conn, project_id_to_be_deleted)
                                    if deleted_project is 0:
                                        print("Project doesn't exists")
                                    else:
                                        print(f"Project {project_id_to_be_deleted} is deleted.")
                                    conn.commit()
                                else:
                                    print("No projects available...")
                                input("\nPress Enter to continue...")
                            elif ch == "9":
                                users = User.view_specific_users(conn)
                                if users is not None and users:
                                    user_ids = [user['user_id'] for user in users if user['role'] == 'member']
                                    user_member_projects = UserProjectWage.view_specific_user_projects(conn, action='assignment_approval', user_ids=user_ids)
                                    if user_member_projects:
                                        user_project_list(conn, user_member_projects)
                                        print("\nEnter User ID and Project ID of Assignment to be Approved : ")
                                        user_id_to_be_issued = None
                                        while user_id_to_be_issued is None:
                                            user_id_to_be_issued = int_input("\nEnter user_id : ")
                                        project_id_to_be_issued = None
                                        while project_id_to_be_issued is None:
                                            project_id_to_be_issued = int_input("\nEnter project_id : ")
                                        updated_user_project = UserProjectWage.change_field_status(conn,
                                                                                                   user_id_to_be_issued,
                                                                                                   project_id_to_be_issued,
                                                                                                   field_name='is_bdo_approved')
                                        if updated_user_project is 0:
                                            print("User Project Assignment doesn't exists")
                                        else:
                                            print(
                                                f"User Project Assignment with user_id:{user_id_to_be_issued} and project_id:{project_id_to_be_issued} is Approved.")
                                        conn.commit()
                                    else:
                                        print("No pending request for Project Assignment Approval.")
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "10":
                                users = User.view_specific_users(conn)
                                if users is not None and users:
                                    user_ids = [user['user_id'] for user in users if user['role'] == 'member']
                                    user_member_projects = UserProjectWage.view_specific_user_projects(conn,
                                                                                                       action='wage_approval',
                                                                                                       user_ids=user_ids)
                                    if user_member_projects:
                                        user_project_list(conn, user_member_projects)
                                        print("\nEnter User ID and Project ID of Assignment to Approve Wage : ")
                                        user_id_to_be_issued = None
                                        while user_id_to_be_issued is None:
                                            user_id_to_be_issued = int_input("\nEnter user_id : ")
                                        project_id_to_be_issued = None
                                        while project_id_to_be_issued is None:
                                            project_id_to_be_issued = int_input("\nEnter project_id : ")
                                        updated_user_project = UserProjectWage.change_field_status(conn,
                                                                                                   user_id_to_be_issued,
                                                                                                   project_id_to_be_issued,
                                                                                                   field_name='is_wage_approved')
                                        if updated_user_project is 0:
                                            print("User Project Assignment doesn't exists")
                                        else:
                                            print(f"User Project Assignment with user_id:{user_id_to_be_issued} and project_id:{project_id_to_be_issued} wage is Approved.")
                                        conn.commit()
                                    else:
                                        print("No pending request for Wage Approval.")
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "11":
                                users = User.view_specific_users(conn)
                                if users is not None and users:
                                    user_ids = [user['user_id'] for user in users if user['role'] == 'member']
                                    user_member_projects = UserProjectWage.view_specific_user_projects(conn,
                                                                                                       action='pending_requests',
                                                                                                       user_ids=user_ids)
                                    user_project_list(conn, user_member_projects)
                                else:
                                    print("No reporting user available...")
                                input("\nPress Enter to continue...")
                            elif ch == "12":
                                complaints = Complaints.view_specific_complaints(conn)
                                if complaints is not None and complaints:
                                    complaint_list(complaints)
                                else:
                                    print("No complaints available...")
                                input("\nPress Enter to continue...")
                            elif ch == "13":
                                Login.logged_in_user = dict()
                                os.system('clear')
                                break
                            else:
                                print("Invalid choice, please choose again\n")
                    elif login_user['role'] == 'gpm':   # Checks if the Logged in user role is GPM
                        while True:
                            os.system('clear')
                            print(f"Welcome ! {login_user['first_name']}...")
                            print("\nMenu"
                                  "\n(1)Assign Member to Project"
                                  "\n(2)View Members on a Project"
                                  "\n(3)Update a Member Assignment on a Project"
                                  "\n(4)Delete Member from a Project"
                                  "\n(5)Issue Job Card for User Project Assignment"
                                  "\n(6)Logout\n")
                            ch = input(">> ").lower().rstrip()
                            if ch == "1":
                                users = User.view_specific_users(conn)
                                if users is not None and users:
                                    user_list(users)
                                else:
                                    print("No reporting user available...")
                                projects = Project.view_specific_projects(conn)
                                if projects:
                                    project_list(projects)
                                else:
                                    print("No projects available...")
                                if users and projects:
                                    new_project_details = new_project_assignment()
                                    new_user_project_wage_id = new_project_details.assign_project(conn)
                                    if new_user_project_wage_id is not None:
                                        print(new_user_project_wage_id)
                                    conn.commit()
                                input("\nPress Enter to continue...")
                            elif ch == "2":
                                user_projects = UserProjectWage.view_specific_user_projects(conn)
                                if user_projects is not None and user_projects:
                                    user_project_list(conn, user_projects)
                                else:
                                    print("No user assigned on a project...")
                                input("\nPress Enter to continue...")
                            elif ch == "3":
                                user_projects = UserProjectWage.view_specific_user_projects(conn, action='update')
                                if user_projects is not None and user_projects:
                                    user_project_list(conn, user_projects)
                                    print("\nEnter User ID and Project ID of Assignment to be updated : ")
                                    user_id_to_be_updated = None
                                    while user_id_to_be_updated is None:
                                        user_id_to_be_updated = int_input("\nEnter user_id : ")
                                    project_id_to_be_updated = None
                                    while project_id_to_be_updated is None:
                                        project_id_to_be_updated = int_input("\nEnter project_id : ")
                                    print("\nSelect Field/(s) to Update:-"
                                          "\n no_of_days_worked"
                                          "\n wage"
                                          "\n attendance"
                                          "\n is_job_card_issued"
                                          "\n is_deleted"
                                          "\n")
                                    fields = ["no_of_days_worked", "wage", "attendance", "is_job_card_issued", "is_deleted", ]
                                    field_to_update = dict()
                                    more = 'y'
                                    while more == 'y':
                                        field_name = input("Enter field name : ").lower().rstrip()
                                        if field_name in fields:
                                            if field_name == 'is_deleted' or field_name == 'is_job_card_issued':
                                                incorrect_field_val = True
                                                while incorrect_field_val:
                                                    field_value = input("Enter field value (Y/N): ").lower().rstrip()
                                                    if field_value == 'y':
                                                        incorrect_field_val = False
                                                        field_value = 1
                                                    elif field_value == 'n':
                                                        incorrect_field_val = False
                                                        field_value = 0
                                                    else:
                                                        incorrect_field_val = True
                                                        print("Invalid Input... Try Again...")
                                            else:
                                                field_value = input("Enter field value : ")
                                                if field_name == 'no_of_days_worked':
                                                    field_to_update['wage'] = int(field_value) * 100.0
                                            field_to_update[field_name] = field_value
                                            more = input("Update more Fields (Y/N) : ").lower().rstrip()
                                        else:
                                            print("\n No such field.. Please try again...")
                                            more = 'y'
                                    updated_user_project = UserProjectWage.update_user_project(conn, user_id_to_be_updated, project_id_to_be_updated, **field_to_update)
                                    if updated_user_project is 0:
                                        print("Assignment doesn't exists")
                                    else:
                                        print(f"User Project Assignment with user_id:{user_id_to_be_updated} and project_id:{project_id_to_be_updated} is updated.")
                                    conn.commit()
                                else:
                                    print("No user assigned on a project...")
                                input("\nPress Enter to continue...")
                            elif ch == "4":
                                user_projects = UserProjectWage.view_specific_user_projects(conn)
                                if user_projects is not None and user_projects:
                                    user_project_list(conn, user_projects)
                                    print("\nEnter User ID and Project ID of Assignment to be deleted : ")
                                    user_id_to_be_deleted = None
                                    while user_id_to_be_deleted is None:
                                        user_id_to_be_deleted = int_input("\nEnter user_id : ")
                                    project_id_to_be_deleted = None
                                    while project_id_to_be_deleted is None:
                                        project_id_to_be_deleted = int_input("\nEnter project_id : ")
                                    deleted_user_project = UserProjectWage.delete_user_project(conn, user_id_to_be_deleted, project_id_to_be_deleted)
                                    if deleted_user_project is 0:
                                        print("User Project Assignment doesn't exists")
                                    else:
                                        print(f"User Project Assignment with user_id:{user_id_to_be_updated} and project_id:{project_id_to_be_updated} is deleted.")
                                    conn.commit()
                                else:
                                    print("No user assigned on a project...")
                                input("\nPress Enter to continue...")
                            elif ch == "5":
                                user_projects = UserProjectWage.view_specific_user_projects(conn)
                                if user_projects is not None and user_projects:
                                    user_projects = [user_project for user_project in user_projects if not user_project['is_job_card_issued']]
                                    user_project_list(conn, user_projects)
                                    print("\nEnter User ID and Project ID of Assignment to be Issued Job Card : ")
                                    user_id_to_be_issued = None
                                    while user_id_to_be_issued is None:
                                        user_id_to_be_issued = int_input("\nEnter user_id : ")
                                    project_id_to_be_issued = None
                                    while project_id_to_be_issued is None:
                                        project_id_to_be_issued = int_input("\nEnter project_id : ")
                                    updated_user_project = UserProjectWage.change_field_status(conn, user_id_to_be_issued, project_id_to_be_issued, field_name='is_job_card_issued')
                                    if updated_user_project is 0:
                                        print("User Project Assignment doesn't exists")
                                    else:
                                        print(f"User Project Assignment with user_id:{user_id_to_be_issued} and project_id:{project_id_to_be_issued} is Issued a Job Card.")
                                        UserProjectWage.show_job_card(conn, user_id_to_be_issued, project_id_to_be_issued)
                                    conn.commit()
                                else:
                                    print("No user assigned on a project...")
                                input("\nPress Enter to continue...")
                            elif ch == "6":
                                Login.logged_in_user = dict()
                                os.system('clear')
                                break
                            else:
                                print("Invalid choice, please choose again\n")
                    elif login_user['role'] == 'member':    # Checks if the Logged in user role is Member
                        while True:
                            os.system('clear')
                            print(f"Welcome ! {login_user['first_name']}...")
                            print("\nMenu"
                                  "\n(1)View my Account Details/Job Cards"
                                  "\n(2)File Complaints/Issues"
                                  "\n(3)Logout\n")
                            ch = input(">> ").lower().rstrip()
                            if ch == "1":
                                user_projects = UserProjectWage.view_user_projects(conn, Login.logged_in_user['user_id'])
                                user_approved_job_cards = [user_project for user_project in user_projects if user_project["is_job_card_issued"]]
                                if user_approved_job_cards:
                                    for job_card in user_approved_job_cards:
                                        UserProjectWage.show_job_card(conn, job_card['user_id'], job_card['project_id'])
                                else:
                                    print("\nNot assigned a Project or Job card not Issued\n")
                                    user = Login.logged_in_user
                                    print("*-------------------------------------------------------*")
                                    print(f"| Username : {user['username']} \t\t\t\t\t|")
                                    print(f"| Name : {user['first_name']} {user['last_name']} \t\t\t\t\t\t|")
                                    print(f"| Email : {user['email']} \t\t\t\t|")
                                    print(f"| Age : {user['age']} \t\t\t\t\t\t|")
                                    print(f"| Gender : {user['gender']} \t\t\t\t\t\t|")
                                    print(f"| Address : {user['area']}-{user['pin_code']} \t\t\t|")
                                    print("*-------------------------------------------------------*")
                                input("\nPress Enter to continue...")
                            elif ch == "2":
                                mem_reporting_heads = Complaints.get_members_bdo_gpm(conn)
                                new_complaint_details = new_complaint(mem_reporting_heads['bdo_user_id'],
                                                                      mem_reporting_heads['gpm_user_id'])
                                new_complaint_id = new_complaint_details.issue_complaints(conn)
                                if new_complaint_id is not None:
                                    print(new_complaint_id)
                                conn.commit()
                                input("\nPress Enter to continue...")
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
            conn.close()    # Closing the DB Connection
            break
        else:
            print("Invalid choice, please choose again\n")


if __name__ == '__main__':
    main()
