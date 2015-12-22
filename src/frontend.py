from flask import Flask, url_for, request
import user

app = Flask(__name__)



@app.route("/")
def hello():
    user_ = user.User('apebabsen', '12345')

    return """
           <p>Hello {u.username}<br />your rfid is {u.rfid}</p>

           <a href="{create_user}">Opprett en bruker</a>
           """.format(u=user_,
                      create_user=url_for('create_user'),
                      )



@app.route("/create/")
def create_user():
    return  """
        <p>Who do you want me to say "Hi" to?</p>

        <form method="POST" action="%s">


        <label for="username">Brukernavn:</label>
        <input type="text" name="username" /><br />

        <label for="rfid">RFID:</label>
        <input type="number" name="rfid" /><br />

        <input type="submit" value="Go!" />

        </form>
        """ % (url_for('create_response'),)

@app.route("/create_response/", methods=['POST'])
def create_response():

    user_ = user.User(request.form["username"], request.form["rfid"])
    try:
        user_.create_in_database()
    except ConnectionError as err:
        return 'Æddabædda! ' + str(err)

    return "Bruker opprettet"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return username

    user_ = user.read_user_from_database(username)

    return user_

if __name__ == "__main__":
    app.run(debug=True)

