import json
import backend


class User:
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
        print(response.text)
        jsonobject = json.loads(response.text)

        if jsonobject["error"]:
            raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

        return jsonobject


        return jsonObject

    def delete_in_database(self):
        parameters = dict(username=self.username)

        response = backend.request('delete_user', data=parameters)
        jsonobject = json.loads(response.text)

        if jsonobject["error"]:
            raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

        return jsonobject


def set_user_pincode(pincode, rfid):
        parameters = dict(pin=pincode, rfid=rfid)

        response = backend.request('update_pin', data=parameters)
        print(response.text)
        jsonObject = json.loads(response.text)

        if jsonObject["error"]:
            raise ConnectionError("Feil i databasen: " + jsonObject["error"])

        return jsonObject

def login_user(rfid, pin):
    parameters = dict(rfid=rfid, pin=pin)

    response = backend.request('login_user', data=parameters)
    print(response.text)
    jsonObject = json.loads(response.text)

    if jsonObject["error"]:
        raise ConnectionError("Feil i databasen: " + jsonObject["error"])

    return jsonObject


def read_user_from_database(sessionID):
    parameters = dict(sess_id=sessionID)

    response = backend.request('get_user_info', data=parameters)
    jsonobject = json.loads(response.text)
    print(response.text)
    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return User(**jsonobject)


def retrive_lended_books_by_user(username):
    parameters = dict(username=username)

    response = backend.request('get_lended_books', data=parameters)
    jsonobject = json.loads(response.text)

    if jsonobject["error"]:
        jsonobject["books"] = {}

    return jsonobject


#read_user_from_database("SXjPhF7GyRDdPNVv8Bmo")