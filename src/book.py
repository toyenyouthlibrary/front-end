import json
import backend
import requests


def lend_book_rfid(bookrfid, userrfid):
    parameters = {
        'book_rfid': bookrfid,
        'user_rfid': userrfid,
    }

    response = backend.request('lend_book', data=parameters)
    jsonobject = json.loads(response.text)

    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return jsonobject


def deliver_book(bookrfid):
    parameters = {
        'book_rfid': bookrfid,
    }

    response = backend.request('deliver_book', data=parameters)
    jsonobject = json.loads(response.text)

    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return jsonobject


def get_book_info(bookrfid):
    parameters = {
        'rfid': bookrfid,
    }

    response = backend.request('get_book_info', data=parameters)
    jsonobject = json.loads(response.text)

    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return jsonobject


def give_feeback(userrfid, bookrfid, ratingtype, value):
    parameters = {
        'user_rfid': userrfid,
        'book_rfid': bookrfid,
        'type': ratingtype,
        'value': value,
    }

    response = backend.request('give_feedback', data=parameters)
    jsonobject = json.loads(response.text)

    if jsonobject["error"]:
        raise ConnectionError('Feil i databasen: ' + jsonobject["error"])

    return jsonobject


def google_books():
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:9788245003642')
    jsonobject = json.loads(r.text)

