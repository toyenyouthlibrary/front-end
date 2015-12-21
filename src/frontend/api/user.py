class User:
    @staticmethod
    def create(username, firstname, lastname, address, phone, email, birth):
        user = User()
        user.username = username
        user.firstname = firstname
        user.lastname = lastname
        user.address = address
        user.phone = phone
        user.email = email
        user.birth = birth

        return user

    @staticmethod
    def parse(object):
        user = User()
        user.username = object["username"]
        user.firstname = object["firstname"]
        user.lastname = object["lastname"]
        user.address = object["address"]
        user.phone = object["phone"]
        user.email = object["email"]
        user.birth = object["birth"]

        return user
