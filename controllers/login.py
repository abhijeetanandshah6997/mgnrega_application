class Login:

    @staticmethod
    def login(conn, username, password):
        cursor_obj = conn.cursor()
        cursor_obj.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
        user = cursor_obj.fetchone()
        cursor_obj.close()
        if user is not None:
            return dict(user)
        else:
            return user
