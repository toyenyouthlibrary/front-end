import json
import backend

class User():
    def __init__(self, username, rfid, database_id=None, **kwargs):
        self.username = username
        self.rfid = rfid
        self.database_id = database_id
        self.details = kwargs


    def __str__(self):
        details_str = ', '.join(['{}: {}'.format(k, v) for k, v in self.details.items()])
        return '{} ({}) - {}'.format(self.username, self.rfid, details_str)


    def create_in_database(self):
        parameters = dict(username=self.username, rfid=self.rfid, **self.details)
        response = backend.request('create_user', data=parameters)
        object = json.loads(response.text)

        if object["error"]:
            raise ConnectionError('Feil i databasen: ' + object["error"])

        return object


    def delete_in_database(self):
        parameters = dict(username=self.username)

        response = backend.request('delete_user', data=parameters)
        object = json.loads(response.text)

        # Parse JSON and throw an exception if the user could not be deleted

        if object["error"]:
            raise ConnectionError('Feil i databasen: ' + object["error"])

        return object


def read_user_from_database(username):
    parameters = dict(username=username)

    response = backend.request('get_user_info', data=parameters)
    object = json.loads(response.text)

    # Parse JSON and create User object, or throw an exception if the user does not exist
    error = object.pop('error')
    if error:
        raise ConnectionError('Feil i databasen: ' + error)

    return User(**object)


