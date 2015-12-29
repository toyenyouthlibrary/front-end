import requests

base_url = "http://www.tryggestad.com/liblog/"
actions = {
    'create_user': 'create_user.php',
    'get_user_info': 'get_user_info.php',
    'delete_user': 'delete_user.php',
    'lend_book': 'lend_book.php',
    'deliver_book': 'deliver_book.php',
}

def request(action, data):
    return requests.post(base_url + actions[action], data=data)

