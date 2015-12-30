from flask import Flask, request, render_template
import book
import user


app = Flask(__name__)


@app.route("/create/")
def create_user():
    return render_template('create_user.html')


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/create_response/", methods=['POST'])
def create_response():
    user_ = user.User(request.form["username"], request.form["rfid"],
                      firstname=request.form["firstname"], email=request.form["email"])
    try:
        user_.create_in_database()
    except ConnectionError as err:
        return 'Æddabædda! ' + str(err)

    return "Bruker {} opprettet".format(user_)

@app.route("/lend_book/")
def lend_book():
    return render_template('lend_book.html')

@app.route("/create_lend_book_response/", methods=['POST'])
def lend_book_response():
    try:
        book_ = book.lend_book_rfid(request.form["bookrfid"], request.form["userrfid"])
    except ConnectionError as err:
        return 'Æddabædda! ' + str(err)

    return "{}".format(book_)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    try:
        user_ = user.read_user_from_database(username)
    except ConnectionError as err:
        return 'Æddabædda! ' + str(err)

    return render_template('user_profile.html', username=user_.username,
                           rfid=user_.rfid, **user_.details)

if __name__ == "__main__":
    app.run(debug=True)

