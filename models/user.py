from datetime import datetime
from sqlite3 import IntegrityError


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

    def add_user(self, conn):
        cursor_obj = conn.cursor()
        try:
            sql_query = '''INSERT INTO user(username, password, email, first_name, last_name, age, gender, contact, area,
                           pin_code, role, created_at, updated_at, is_deleted) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            sql_params = (self.username, self.password, self.email, self.first_name, self.last_name, self.age, self.gender,
                          self.contact, self.area, self.pin_code, self.role, self.created_at, self.updated_at,
                          self.is_deleted, )
            cursor_obj.execute(sql_query, sql_params)
            user_id = cursor_obj.lastrowid
            cursor_obj.close()
            return user_id
        except IntegrityError:
            print(IntegrityError)

    @staticmethod
    def view_specific_users(conn, **kwargs):
        role = kwargs.get('role', None)
        if role:
            sql_query = '''SELECT user_id, username FROM user WHERE role=? AND is_deleted=False'''
            sql_params = (role, )
            cursor_obj = conn.cursor()
            cursor_obj.execute(sql_query, sql_params)
            users = cursor_obj.fetchall()
            cursor_obj.close()
            # if users is not None:
            #     return (users)
            # else:
            return users

    def view_user_details(self, conn, username):
        pass

    def update_user(self, conn, **kwargs):
        pass

    @staticmethod
    def delete_user(conn, username):
        if username:
            sql_query = '''UPDATE user SET is_deleted=True WHERE username=?'''
            sql_params = (username, )
            cursor_obj = conn.cursor()
            cursor_obj.execute(sql_query, sql_params)
            update_row_count = cursor_obj.rowcount
            cursor_obj.close()
            # if users is not None:
            #     return (users)
            # else:
            return update_row_count
