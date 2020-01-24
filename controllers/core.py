class Core:

    @staticmethod
    def query_runner(conn, sql_query, sql_params):
        cursor_obj = conn.cursor()
        if sql_params is None:
            cursor_obj.execute(sql_query)
        else:
            cursor_obj.execute(sql_query, sql_params)
        return cursor_obj
