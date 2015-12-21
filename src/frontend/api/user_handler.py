import json
import requests
from api.user import User

base_url = "http://www.tryggestad.com/liblog/"
create_user_path = "create_user.php"
get_user_path = "get_user.php"
delete_user_path = "delete_user.php"


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
        dictionary = json.loads(response.text)

        # Parse JSON and throw an exception if the user could not be created

        if dictionary["error"] > 0:
            raise Exception(dictionary["message"])

        return User.create(username, firstname, lastname, address, phone, email, birth)


    @staticmethod
    def delete_user(username):
        parameters = {
            'username': username,
        }

        response = requests.post(base_url + delete_user_path, data=parameters)
        dictionary = json.loads(response.text)

        # Parse JSON and throw an exception if the user could not be deleted

        if dictionary["error"] > 0:
            raise Exception(dictionary["message"])




    @staticmethod
    def get_user(username):
        parameters = {
            'username': username
        }

        response = requests.post(base_url + get_user_path, data=parameters)
        dictionary = json.loads(response.text)

        # Parse JSON and create User object, or throw an exception if the user does not exist

        if dictionary["error"] > 0:
            raise Exception(dictionary["message"])

        return User.parse(dictionary.user)

