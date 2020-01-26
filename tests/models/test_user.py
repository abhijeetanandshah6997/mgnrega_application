import unittest
import sqlite3
from models.user import User


class TestUser(unittest.TestCase):

    def setUp(self) -> None:
        self.conn = sqlite3.connect('mgnrega.sqlite')

    def test_add_user(self):
        test_user = User('uname', 'pass', 'test@mgnrega.com', 'fname', 'lname', 24, 'M', '+91-9023221234', 'India',
                         '456754', 'bdo')
        assert type(test_user) == User