class Core:

    @staticmethod
    def query_runner(conn, sql_query, sql_params):
        """
        a function that take in sql_query and sql_params and executes it on the db connection cursor object
        :param conn: a sqlite db connection object
        :param sql_query: sql statement to be executed
        :param sql_params: sql params tuples to be inserted in the sql statement
        :return: a cursor object with the fetched data from db
        """
        cursor_obj = conn.cursor()
        if sql_params is None:
            cursor_obj.execute(sql_query)
        else:
            cursor_obj.execute(sql_query, sql_params)
        return cursor_obj
