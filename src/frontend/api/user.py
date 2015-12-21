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
    def parse(dictionary):
        user = User()
        user.username = dictionary["username"]
        user.firstname = dictionary["firstname"]
        user.lastname = dictionary["lastname"]
        user.address = dictionary["address"]
        user.phone = dictionary["phone"]
        user.email = dictionary["email"]
        user.birth = dictionary["birth"]

        return user
