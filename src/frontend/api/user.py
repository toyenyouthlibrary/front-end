class User:
    @staticmethod
    def create(name, email, phone, password):
        user = User()
        user.name = name
        user.email = email
        user.phone = phone
        user.password = password
        return user

    @staticmethod
    def parse(object):
        user = User()
        user.name = object["name"]
        user.email = object["email"]
        user.phone = object["phone"]
        user.password = object["password"]
        return user
