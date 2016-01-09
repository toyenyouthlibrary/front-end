import json
import backend

def admin_login(username, password):
    parameters = {'user': username, 'pass': password}
    response = backend.request('admin_login', data=parameters)
    object = json.loads(response.text[3:])
    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def admin_fetch_all_books(userID):
    parameters = {'id': userID}
    response = backend.request('admin_get_all_books', data=parameters)

    object = json.loads(response.text[6:])
    print(object)
    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object