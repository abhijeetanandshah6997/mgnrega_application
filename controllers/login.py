from controllers.core import Core


class Login:

    logged_in_user = dict()

    @staticmethod
    def login(conn, username, password):
        sql_query = '''SELECT * FROM user WHERE username=? AND password=?'''
        sql_params = (username, password, )
        cursor_obj = Core.query_runner(conn, sql_query, sql_params)
        user = cursor_obj.fetchone()
        cursor_obj.close()
        if user is not None:
            if user['is_deleted'] == 0:
                Login.logged_in_user = dict(user)
                return dict(user)
            else:
                return 'access_denied'
        else:
            return user

    @staticmethod
    def logout():
        Login.logged_in_user = dict()
        print("Logout Successful...")
