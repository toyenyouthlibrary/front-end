import requests

base_url = "http://www.tryggestad.com/liblog/"
actions = {
    'create_user': 'create_user.php',
    'get_user_info': 'get_user.php',
    'delete_user': 'delete_user.php',
}

def request(action, data):
    return requests.post(base_url + actions[action], data=data)

