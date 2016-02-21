import json
import backend


def admin_login(username, password):
    parameters = {'user_old': username, 'pass': password}
    response = backend.request('admin_login', data=parameters)
    jsonobject = json.loads(response.text)

    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return jsonobject


def admin_fetch_all_books(userid):
    parameters = {'id': userid}
    response = backend.request('admin_get_all_books', data=parameters)

    jsonobject = json.loads(response.text)
    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return jsonobject


def admin_get_lent_books(userid):
    parameters = {'id': userid}
    response = backend.request('admin_get_lent_books', data=parameters)

    jsonobject = json.loads(response.text)
    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return jsonobject


def admin_get_users(userid):
    parameters = {'id': userid}
    response = backend.request('admin_get_all_users', data=parameters)

    jsonobject = json.loads(response.text)

    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return jsonobject
