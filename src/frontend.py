from flask import Flask, url_for, request, render_template
import book
import user


app = Flask(__name__)


def url_list():
    return {
        'url_css': url_for('static', filename='style.css'),
        'url_create_user': url_for('create_user'),
        'url_frontpage': url_for('welcome'),
        'url_create_response': url_for('create_response'),
        'url_lend_book_response': url_for('lend_book_response'),


    }

@app.route("/create/")
def create_user():
    return render_template('create_user.html', **url_list())


@app.route("/")
def welcome():
    return render_template('welcome.html', **url_list())

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
    return render_template('lend_book.html', **url_list())

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

    return render_template('user_profile.html', **url_list(),
                           username=user_.username, **user_.details)

if __name__ == "__main__":
    app.run(debug=True)

