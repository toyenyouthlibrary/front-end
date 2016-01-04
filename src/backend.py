import requests

base_url = "http://norbye.com/-other-/liblog/"
actions = {
    'create_user': 'create_user.php',
    'get_user_info': 'get_user_info.php',
    'delete_user': 'delete_user.php',
    'lend_book': 'lend_book.php',
    'deliver_book': 'deliver_book.php',
    'get_lended_books': 'get_lended_books.php',
}

def request(action, data):
    return requests.post(base_url + actions[action], data=data)

