from datetime import datetime
from sqlite3 import IntegrityError

from controllers.login import Login
from controllers.core import Core
from models.project import Project
from models.user import User


class UserProjectWage:

    def __init__(self, user_id, project_id, no_of_days_worked, wage, attendance):
        self.user_id = user_id
        self.project_id = project_id
        self.no_of_days_worked = no_of_days_worked
        self.wage = wage
        self.attendance = attendance
        self.is_bdo_approved = False
        self.is_wage_approved = False
        self.is_job_card_issued = False
        self.is_deleted = False

    def assign_project(self, conn):
        try:
            sql_query = '''INSERT INTO user_project_wage(user_id, project_id, no_of_days_worked, wage, attendance, is_bdo_approved, is_wage_approved, is_job_card_issued, is_deleted) VALUES(?,?,?,?,?,?,?,?,?)'''
            sql_params = (self.user_id, self.project_id, self.no_of_days_worked, self.wage, self.attendance, self.is_bdo_approved, self.is_wage_approved, self.is_job_card_issued, self.is_deleted, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            user_project_wage_id = cursor_obj.lastrowid
            cursor_obj.close()
            return user_project_wage_id
        except IntegrityError:
            print(IntegrityError)

    @staticmethod
    def view_specific_user_projects(conn, **kwargs):
        action = kwargs.get('action', None)
        if not action == 'assignment_approval' and not action == 'wage_approval' and not action == 'pending_requests':
            sql_query_user = '''SELECT * FROM gpm_mem_rel WHERE gpm_user_id=?'''
            sql_params_user = (Login.logged_in_user['user_id'],)
            cursor_obj_user = Core.query_runner(conn, sql_query_user, sql_params_user)
            user_ids = [user['mem_user_id'] for user in cursor_obj_user.fetchall()]
            cursor_obj_user.close()
        else:
            user_ids = kwargs.get('user_ids', [])
        if user_ids:
            if len(user_ids) > 1:
                sql_query = f'''SELECT * FROM user_project_wage WHERE user_id IN {str(tuple(user_ids))}'''
            else:
                sql_query = f'''SELECT * FROM user_project_wage WHERE user_id={user_ids[0]}'''
            if not action == 'update':
                sql_query = sql_query + ''' AND is_deleted=False'''
                if action == 'pending_requests':
                    sql_query = sql_query + ''' AND is_wage_approved=False OR is_bdo_approved=False'''
                elif action == 'wage_approval':
                    sql_query = sql_query + ''' AND is_wage_approved=False'''
                elif action == 'assignment_approval':
                    sql_query = sql_query + ''' AND is_bdo_approved=False'''
            cursor_obj = Core.query_runner(conn, sql_query, sql_params=None)
            user_projects = cursor_obj.fetchall()
            cursor_obj.close()
            return user_projects

    @staticmethod
    def update_user_project(conn, user_id, project_id, **kwargs):
        if project_id is not None and user_id is not None:
            update_param = str()
            new_values = list()
            for key, value in kwargs.items():
                update_param = update_param + key + "=?,"
                new_values.append(value)
            update_param = update_param[:-1]
            sql_query = f'''UPDATE user_project_wage SET ''' + update_param + ''' WHERE user_id=? AND project_id=?'''
            sql_params = tuple(new_values) + (user_id, project_id,)
            print(sql_query)
            print(sql_params)
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            update_row_count = cursor_obj.rowcount
            cursor_obj.close()
            return update_row_count

    @staticmethod
    def delete_user_project(conn, user_id, project_id):
        if project_id is not None and user_id is not None:
            sql_query = '''UPDATE user_project_wage SET is_deleted=True WHERE user_id=? AND project_id=?'''
            sql_params = (user_id, project_id, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            update_row_count = cursor_obj.rowcount
            cursor_obj.close()
            return update_row_count

    @staticmethod
    def view_user_project_details(conn, user_id, project_id):
        if project_id is not None and user_id is not None:
            sql_query = '''SELECT * FROM user_project_wage WHERE user_id=? AND project_id=?'''
            sql_params = (user_id, project_id,)
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            user_project = cursor_obj.fetchone()
            cursor_obj.close()
            return user_project

    @staticmethod
    def change_field_status(conn, user_id, project_id, **kwargs):
        field_name = kwargs.get('field_name', None)
        if project_id is not None and user_id is not None:
            sql_query = '''UPDATE user_project_wage SET ''' + field_name + '''=True WHERE user_id=? AND project_id=?'''
            sql_params = (user_id, project_id,)
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            update_row_count = cursor_obj.rowcount
            cursor_obj.close()
            return update_row_count

    @staticmethod
    def show_job_card(conn, user_id, project_id):
        if project_id is not None and user_id is not None:
            user_project = UserProjectWage.view_user_project_details(conn, user_id, project_id)
            if bool(user_project['is_job_card_issued']):
                user = User.view_user_details(conn, user_id)
                project = Project.view_project_details(conn, project_id)
                print("*-------------------------------------------------------*")
                print(f"| Username : {user['username']} \t\t\t\t\t|")
                print(f"| Name : {user['first_name']} {user['last_name']} \t\t\t\t\t\t|")
                print(f"| Email : {user['email']} \t\t\t\t|")
                print(f"| Age : {user['age']} \t\t\t\t\t\t|")
                print(f"| Gender : {user['gender']} \t\t\t\t\t\t|")
                print(f"| Address : {user['area']}-{user['pin_code']} \t\t\t|")
                print(f"| Project Name : {project['project_name']} \t\t\t|")
                print(f"| Project Type : {project['project_type']} \t\t\t|")
                print("*-------------------------------------------------------*")
            else:
                print("Request GPM for Job Card...")
