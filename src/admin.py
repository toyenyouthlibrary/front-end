import json
import backend

def admin_login(username, password):
    parameters = {'user': username, 'pass': password}
    response = backend.request('admin_login', data=parameters)
    object = json.loads(response.text)
    print(object)
    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def admin_fetch_all_books(userID):
    parameters = {'id': userID}
    response = backend.request('admin_get_all_books', data=parameters)

    object = json.loads(response.text)
    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def admin_get_lent_books(userID):
    parameters = {'id': userID}
    response = backend.request('admin_get_lent_books', data=parameters)

    object = json.loads(response.text)
    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def admin_get_users(userID):
    parameters = {'id': userID}
    response = backend.request('admin_get_all_users', data=parameters)

    object = json.loads(response.text)

    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

#109342903234
print(admin_fetch_all_books("109342903234"))