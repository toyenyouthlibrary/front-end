import flask
import book
import user
import flask_wtf
import wtforms
import random

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'temmelighemmelig'


@app.route("/create/", methods=['GET', 'POST'])
def create_user():
    if flask.request.form:
        user_ = user.User(rfid=int(random.randint(0, 100000000000 - 1)), **flask.request.form)
        try:
            user_.create_in_database()
        except ConnectionError as err:
            return flask.render_template('error.html', error=err)

        flask.flash("Bruker med navn {} og RFID {} opprettet".format(user_.username, user_.rfid))
        return flask.redirect(flask.url_for('create_user'))

    return flask.render_template('create_user.html')


@app.route("/")
def welcome():
    return flask.render_template('welcome.html')

class FormLendBook(flask_wtf.Form):
    book_rfid = wtforms.IntegerField('Bok RFID' , validators=[wtforms.validators.number_range(0)])
    user_rfid = wtforms.IntegerField('Bruker RFID ', validators=[wtforms.validators.DataRequired()])

@app.route("/lend_book/", methods=['GET', 'POST'])
def lend_book():
    form = FormLendBook()
    if form.validate_on_submit():
        try:
            book_ = book.lend_book_rfid(flask.request.form["book_rfid"], flask.request.form["user_rfid"])
            flask.flash("Bok lånt!")
        except ConnectionError as err:
            return flask.render_template('error.html', error=err)
        flask.redirect(flask.url_for('lend_book'))

    return flask.render_template('lend_book.html', form = form)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    try:
        #Will return a array containing all the book dicts
        books = user.retrive_lended_books_by_user(username)

    except ConnectionError as err:
        return flask.render_template('error.html', error=err)

    try:
        user_ = user.read_user_from_database(username)
    except ConnectionError as err:
        return flask.render_template('error.html', error=err)


    return flask.render_template('user_profile.html', username=user_.username,
                           rfid=user_.rfid, **user_.details, books=books)

if __name__ == "__main__":
    app.run(debug=True)
