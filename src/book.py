import json
import backend
import requests


def lend_book_rfid(bookRFID, userRFID):
    parameters = {
        'book_rfid': bookRFID,
        'user_rfid': userRFID,
    }

    response = backend.request('lend_book', data=parameters)
    response = response.text.replace(response.text[:3], '')
    object = json.loads(response)

    if object["error"]:
            raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def deliver_book(bookRFID):
    parameters = {
        'book_rfid': bookRFID,
    }

    response = backend.request('deliver_book', data=parameters)
    response = response.text.replace(response.text[:3], '')
    object = json.loads(response)

    if object["error"]:
        raise ConnectionError('Feil i databasen: ' + object["error"])

    return object

def get_book_info():
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:9788245003642')
    print(r.text)
    object = json.loads(r.text)


print(get_book_info())