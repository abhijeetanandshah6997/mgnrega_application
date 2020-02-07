import unittest
import mock

from controllers.login import Login


class MockData:

    @staticmethod
    @mock.patch('sqlite3.connect')
    def get_db_connection(mock_db):
        return mock_db

    @staticmethod
    def get_username():
        return 'test_username'

    @staticmethod
    def get_password():
        return 'test_password'

    @staticmethod
    def get_access():
        return 'access_denied'

    @staticmethod
    def fetchone():
        return {'user_id': 1, 'username': 'bdo_admin', 'password': 'admin123', 'email': 'bdo@mgnrega.com',
                'first_name': 'BDO', 'last_name': 'ADMIN', 'age': '', 'gender': '', 'contact': '', 'area': None,
                'pin_code': None, 'role': 'bdo', 'created_at': '', 'updated_at': None, 'is_deleted': 0}

    @staticmethod
    def fetchone_deleted():
        return {'user_id': 1, 'username': 'bdo_admin', 'password': 'admin123', 'email': 'bdo@mgnrega.com',
                'first_name': 'BDO', 'last_name': 'ADMIN', 'age': '', 'gender': '', 'contact': '', 'area': None,
                'pin_code': None, 'role': 'bdo', 'created_at': '', 'updated_at': None, 'is_deleted': 1}


class TestLogin(unittest.TestCase):

    @mock.patch('controllers.login.Core')
    def test_login_user(self, mock_core):
        mock_core.query_runner().fetchone.return_value = MockData.fetchone()
        user = Login.login(MockData.get_db_connection(), MockData.get_username(), MockData.get_password())
        assert user is not None
        assert isinstance(user, (dict,))

    @mock.patch('controllers.login.Core')
    def test_login_user_deleted(self, mock_core):
        mock_core.query_runner().fetchone.return_value = MockData.fetchone_deleted()
        user = Login.login(MockData.get_db_connection(), MockData.get_username(), MockData.get_password())
        assert user is not None
        assert isinstance(MockData.get_access(), (str, ))
        assert MockData.get_access() == user

    @mock.patch('controllers.login.Core')
    def test_login_user_none(self, mock_core):
        mock_core.query_runner().fetchone.return_value = None
        user = Login.login(MockData.get_db_connection(), MockData.get_username(), MockData.get_password())
        assert user is None

    @mock.patch('controllers.login.Login')
    def test_logout(self, mock_login):
        user = mock_login.logged_in_user = dict()
        Login.logout()
        assert isinstance(user, (dict, ))


if __name__ == '__main__':
    unittest.main()
