import json
import backend

# TODO - Return an error message in JSON {"errors": "some string"} (Ask Tor)

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

