from datetime import datetime
from sqlite3 import IntegrityError

from controllers.login import Login
from controllers.core import Core


class User:

    def __init__(self, username, password, email, first_name, last_name, age, gender, contact, area, pin_code,
                 role='member'):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.contact = contact
        self.area = area
        self.pin_code = pin_code
        self.role = role
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_deleted = False

    def add_user(self, conn, gpm_user_id):
        try:
            sql_query = '''INSERT INTO user(username, password, email, first_name, last_name, age, gender, contact, area,
                           pin_code, role, created_at, updated_at, is_deleted) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            sql_params = (self.username, self.password, self.email, self.first_name, self.last_name, self.age, self.gender,
                          self.contact, self.area, self.pin_code, self.role, self.created_at, self.updated_at,
                          self.is_deleted, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            user_id = cursor_obj.lastrowid
            cursor_obj.close()
            sql_query_rel = str()
            sql_params_rel = tuple()
            if Login.logged_in_user['role'] == 'bdo' and self.role == 'gpm':
                sql_query_rel = '''INSERT INTO bdo_gpm_rel(bdo_user_id, gpm_user_id) VALUES(?,?)'''
                sql_params_rel = (Login.logged_in_user['user_id'], user_id,)
            elif Login.logged_in_user['role'] == 'bdo' and self.role == 'member':
                sql_query_rel = '''INSERT INTO gpm_mem_rel(gpm_user_id, mem_user_id) VALUES(?,?)'''
                sql_params_rel = (gpm_user_id, user_id,)
            cursor_obj_rel = Core.query_runner(conn, sql_query_rel, sql_params_rel)
            cursor_obj_rel.close()
            return user_id
        except IntegrityError:
            print(IntegrityError)

    @staticmethod
    def view_specific_users(conn, **kwargs):
        action = kwargs.get('action', None)
        sql_query = str()
        if Login.logged_in_user['role'] == 'bdo':
            sql_query = '''SELECT * FROM bdo_gpm_rel WHERE bdo_user_id=?'''
        elif Login.logged_in_user['role'] == 'gpm':
            sql_query = '''SELECT * FROM gpm_mem_rel WHERE gpm_user_id=?'''
        sql_params = (Login.logged_in_user['user_id'], )
        cursor_obj = Core.query_runner(conn, sql_query, sql_params)
        user_ids = list()
        if Login.logged_in_user['role'] == 'bdo':
            gpm_user_ids = [user['gpm_user_id'] for user in cursor_obj.fetchall()]
            sql_query_mem = f'''SELECT * FROM gpm_mem_rel WHERE gpm_user_id IN {str(tuple(gpm_user_ids))}'''
            cursor_obj_mem = Core.query_runner(conn, sql_query_mem, sql_params=None)
            mem_user_ids = [user['mem_user_id'] for user in cursor_obj_mem.fetchall()]
            cursor_obj_mem.close()
            user_ids = list(set().union(gpm_user_ids, mem_user_ids))
        elif Login.logged_in_user['role'] == 'gpm':
            user_ids = [user['mem_user_id'] for user in cursor_obj.fetchall()]
        cursor_obj.close()
        if user_ids:
            if len(user_ids) > 1:
                sql_query_user = f'''SELECT user_id, username, role FROM user WHERE user_id IN {str(tuple(user_ids))}'''
            else:
                sql_query_user = f'''SELECT user_id, username, role FROM user WHERE user_id={user_ids[0]}'''
            if not action == 'update':
                sql_query_user = sql_query_user + ''' AND is_deleted=False'''
            cursor_obj_user = Core.query_runner(conn, sql_query_user, sql_params=None)
            users = cursor_obj_user.fetchall()
            cursor_obj_user.close()
            return users
        else:
            return None

    @staticmethod
    def view_user_details(conn, user_id):
        if user_id is not None:
            sql_query = '''SELECT * FROM user WHERE user_id=?'''
            sql_params = (user_id, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            user = cursor_obj.fetchone()
            cursor_obj.close()
            return user

    @staticmethod
    def update_user(conn, username, **kwargs):
        if username is not None:
            updated_at = datetime.now()
            update_param = str()
            new_values = list()
            for key, value in kwargs.items():
                update_param = update_param + key + "=?,"
                new_values.append(value)
            update_param = update_param + "updated_at=?"
            sql_query = f'''UPDATE user SET ''' + update_param + ''' WHERE username=?'''
            sql_params = tuple(new_values) + (str(updated_at), str(username), )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            update_row_count = cursor_obj.rowcount
            cursor_obj.close()
            return update_row_count

    @staticmethod
    def delete_user(conn, username):
        if username:
            updated_at = datetime.now()
            sql_query = '''UPDATE user SET is_deleted=True,updated_at=? WHERE username=?'''
            sql_params = (updated_at, username, )
            cursor_obj = Core.query_runner(conn, sql_query, sql_params)
            update_row_count = cursor_obj.rowcount
            cursor_obj.close()
            return update_row_count
