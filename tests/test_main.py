import unittest
import sqlite3
from main import DataBaseClass


class TestDatabaseClass(unittest.TestCase):

    def setUp(self) -> None:
        self.conn = sqlite3.connect('mgnrega.sqlite')

    def tearDown(self) -> None:
        cursor_obj = self.conn.cursor()
        cursor_obj.close()
        self.conn.commit()

    def test_db_connection(self):
        assert DataBaseClass.db_connection().cursor().fetchall() == self.conn.cursor().fetchall()


if __name__ == '__main__':
    unittest.main()
