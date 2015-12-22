import json
import requests
from src.frontend.api.user import User

base_url = "http://www.tryggestad.com/liblog/"
create_user_path = "create_user.php"
get_user_path = "get_user.php"
delete_user_path = "delete_user.php"


class UserHandler:
    @staticmethod
    def create_user(name, email, phone, password):
        parameters = {

            'name': name,
            'email': email,
            'phone': phone,
            'password': password,

        }

        response = requests.post(base_url + create_user_path, data=parameters)
        object = json.loads(response.text)

        '''
        If error contains a number higher than 0, it means that something went wrong.
        Throw an exception with the message
        '''

        if object["error"] > "0":
            raise Exception(object["message"])

        # return User.create(password, email, phone, name)
        return object

    @staticmethod
    def delete_user(username):
        parameters = {
            'username': username,
        }

        response = requests.post(base_url + delete_user_path, data=parameters)
        object = json.loads(response.text)

        # Parse JSON and throw an exception if the user could not be deleted
        '''
        if object["error"] > "0":
            raise Exception(object["message"])
        '''

        return object


    @staticmethod
    def get_user(username):
        parameters = {
            'username': username
        }

        response = requests.post(base_url + get_user_path, data=parameters)
        object = json.loads(response.text)

        # Parse JSON and create User object, or throw an exception if the user does not exist

        '''
        if object["error"] > "0":
            raise Exception(object["message"])
        '''

        # return User.parse(object.user)
        return object

userHandler = UserHandler()
print(userHandler.create_user("", "", "", ""))