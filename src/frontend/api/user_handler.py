import json
import requests
from api.user import User

base_url = "*"
base_url = "http://www.tryggestad.com/liblog/"
create_user_path = "create_user.php"
get_user_path = "get_user.php"


class UserHandler:
    @staticmethod
    def create_user(username, firstname, lastname, address, phone, email, birth):
        parameters = {
            'username': username,
            'firstname': firstname,
            'lastname': lastname,
            'address': address,
            'phone': phone,
            'email': email,
            'birth': birth
        }

        response = requests.post(base_url + create_user_path, data=parameters)

        """
        TODO: Parse JSON and throw an exception if the user could not be created
        """

        return User.create(username, firstname, lastname, address, phone, email, birth)

    @staticmethod
    def get_user(username):
        parameters = {
            'username': username
        }

        response = requests.post(base_url + get_user_path, data=parameters)

        """
        TODO: Parse JSON and create User object, or throw exception if the user does not exist
        """

        return User.parse(json.loads(response))
