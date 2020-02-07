import sqlite3
import unittest
import mock

from controllers.core import Core


class MockData:

    @staticmethod
    @mock.patch('sqlite3.connect')
    def get_db_connection(mock_db):
        return mock_db

    # @staticmethod
    # @mock.patch('sqlite3.Cursor')
    # def get_db_cursor(mock_cursor):
    #     return mock_cursor

    @staticmethod
    def get_sql_query():
        test_sql_query = "test_string"
        return test_sql_query

    @staticmethod
    def get_sql_params():
        test_sql_params = ("test_sql_params", )
        return test_sql_params


class TestCore(unittest.TestCase):

    @mock.patch('sqlite3.connect')
    def test_query_runner(self, mock_cursor):
        mock_cursor.cursor().execute.return_value = sqlite3.Cursor
        cursor_obj = Core.query_runner(MockData.get_db_connection(), MockData.get_sql_query(), MockData.get_sql_params())
        assert isinstance(cursor_obj, (sqlite3.Cursor, ))


if __name__ == '__main__':
    unittest.main()
