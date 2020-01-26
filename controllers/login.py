from controllers.core import Core


class Login:

    logged_in_user = dict()

    @staticmethod
    def login(conn, username, password):
        """
        a function that validates the login credentials i.e. username and password from the user table in the database
        :param conn: a sqlite db connection object
        :param username: username of the login user
        :param password: password to validate the user authenticity
        :return: a dictionary that contains logged in user details with **role** in the application
        """
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
        """
        function that clears the global class object of the Login class thereby removing the logged in user details
        """
        Login.logged_in_user = dict()
        print("Logout Successful...")
