import flask
import book
import user


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'temmelighemmelig'


@app.route("/create/", methods=['GET', 'POST'])
def create_user():
    if flask.request.form:
        user_ = user.User(**flask.request.form)
        try:
            user_.create_in_database()
        except ConnectionError as err:
            return 'Æddabædda! ' + str(err)

        flask.flash("Bruker {} opprettet".format(user_))
        return flask.redirect(flask.url_for('create_user'))

    return flask.render_template('create_user.html')


@app.route("/")
def welcome():
    return flask.render_template('welcome.html')

@app.route("/lend_book/")
def lend_book():
    return flask.render_template('lend_book.html')

@app.route("/create_lend_book_response/", methods=['POST'])
def lend_book_response():
    try:
        book_ = book.lend_book_rfid(flask.request.form["bookrfid"], flask.request.form["userrfid"])
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

    return flask.render_template('user_profile.html', username=user_.username,
                           rfid=user_.rfid, **user_.details)

if __name__ == "__main__":
    app.run(debug=True)

