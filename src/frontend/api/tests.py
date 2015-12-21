import unittest
from api.user_handler import UserHandler

test_username = "apitest"
test_firstname = "api"
test_lastname = "test"
test_address = "NULL"
test_telephone = "NULL"
test_email = "NULL"
test_birth = "NULL"


class Tests(unittest.TestCase):
    """
    Tests to see if the 'create_user' function
    actually creates a User object
    """
    def test_user_handler(self):
        user = UserHandler.create_user(test_username, test_firstname,
                                       test_lastname, test_address,
                                       test_telephone, test_email,
                                       test_birth)

        self.assertNotEqual(None, user)

        user_equivalent = UserHandler.get_user(test_username)

        self.assertEqual(user, user)
