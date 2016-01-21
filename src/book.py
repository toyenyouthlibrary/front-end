import json
import backend
import requests


def lend_book_rfid(bookRFID, userRFID):
    parameters = {
        'book_rfid': bookRFID,
        'user_rfid': userRFID,
    }

    response = backend.request('lend_book', data=parameters)
    object = json.loads(response.text)

    if object["error"]:
            raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def deliver_book(bookRFID):
    parameters = {
        'book_rfid': bookRFID,
    }

    response = backend.request('deliver_book', data=parameters)
    object = json.loads(response.text)

    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def get_book_info(bookRFID):
    parameters = {
        'rfid': bookRFID,
    }

    response = backend.request('get_book_info', data=parameters)
    object = json.loads(response.text)

    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def give_feeback(user_rfid, book_rfid, type, value):
    parameters = {
        'user_rfid': user_rfid,
        'book_rfid': book_rfid,
        'type': type,
        'value': value,
    }

    response = backend.request('give_feedback', data=parameters)
    object = json.loads(response.text)

    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def google_books():
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:9788245003642')
    object = json.loads(r.text)

