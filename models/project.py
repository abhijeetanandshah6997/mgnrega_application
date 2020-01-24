from datetime import datetime
from sqlite3 import IntegrityError

from controllers.login import Login
from controllers.core import Core


class Project:

    def __init__(self, project_name, project_type, area, total_required_member, cost_estimate, start_date, end_date_estimate):
        self.project_name = project_name
        self.project_type = project_type
        self.area = area
        self.total_required_member = total_required_member
        self.cost_estimate = cost_estimate
        self.start_date = start_date
        self.end_date_estimate = end_date_estimate
        self.created_by = Login.logged_in_user['user_id']
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_deleted = False

    def add_project(self, conn):
        try:
            sql_query = '''INSERT INTO project(project_name, project_type, area, total_required_member, cost_estimate,
                        start_date, end_date_estimate, created_by, created_at, updated_at, is_deleted) 
                        VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
            sql_params = (self.project_name, self.project_type, self.area, self.total_required_member,
                          self.cost_estimate, self.start_date, self.end_date_estimate, self.created_by, self.created_at, self.updated_at,
                          self.is_deleted, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            project_id = cursor_obj.lastrowid
            cursor_obj.close()
            return project_id
        except IntegrityError:
            print(IntegrityError)

    @staticmethod
    def view_specific_projects(conn, **kwargs):
        action = kwargs.get('action', None)
        sql_params = None
        if Login.logged_in_user['role'] == 'bdo':
            sql_params = (Login.logged_in_user['user_id'],)
        elif Login.logged_in_user['role'] == 'gpm':
            sql_query_user = '''SELECT * FROM bdo_gpm_rel WHERE gpm_user_id=?'''
            sql_params_user = (Login.logged_in_user['user_id'],)
            cursor_obj_user = Core.query_runner(conn, sql_query_user, sql_params_user)
            user = cursor_obj_user.fetchone()
            cursor_obj_user.close()
            sql_params = (user['bdo_user_id'], )
        if sql_params is not None:
            if action == 'update':
                sql_query = '''SELECT * FROM project WHERE created_by=?'''
            else:
                sql_query = '''SELECT * FROM project WHERE created_by=? AND is_deleted=False'''
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            projects = cursor_obj.fetchall()
            cursor_obj.close()
            return projects

    @staticmethod
    def view_project_details(conn, project_id):
        if project_id is not None:
            sql_query = '''SELECT * FROM project WHERE project_id=?'''
            sql_params = (project_id, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            project = cursor_obj.fetchone()
            cursor_obj.close()
            return project

    @staticmethod
    def update_project(conn, project_id, **kwargs):
        if project_id is not None:
            updated_at = datetime.now()
            update_param = str()
            new_values = list()
            for key, value in kwargs.items():
                update_param = update_param + key + "=?,"
                new_values.append(value)
            update_param = update_param + "updated_at=?"
            sql_query = f'''UPDATE project SET ''' + update_param + ''' WHERE project_id=?'''
            sql_params = tuple(new_values) + (str(updated_at), project_id, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            update_row_count = cursor_obj.rowcount
            cursor_obj.close()
            return update_row_count

    @staticmethod
    def delete_project(conn, project_id):
        if project_id:
            updated_at = datetime.now()
            sql_query = '''UPDATE project SET is_deleted=True,updated_at=? WHERE project_id=?'''
            sql_params = (updated_at, project_id, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            update_row_count = cursor_obj.rowcount
            cursor_obj.close()
            return update_row_count
