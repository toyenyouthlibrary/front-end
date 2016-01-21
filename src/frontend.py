import flask
import book
import user
import flask_wtf
import wtforms
import random
import admin
from flask_table import Table, Col, LinkCol

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'temmelighemmelig'


@app.route("/create/", methods=['GET', 'POST'])
def create_user():
    if flask.request.form:
        user_ = user.User(rfid=int(random.randint(0, 100000000000 - 1)), **flask.request.form)
        try:
            user_.create_in_database()
        except ConnectionError as err:
            return flask.render_template('user/error.html', error=err)

        flask.flash("Bruker med navn {} og RFID {} opprettet".format(user_.username, user_.rfid))
        return flask.redirect(flask.url_for('create_user'))

    return flask.render_template('user/create_user.html')


@app.route("/")
def welcome():
    return flask.render_template('user/welcome.html')


class FormLendBook(flask_wtf.Form):
    book_rfid = wtforms.IntegerField('Bok RFID', validators=[wtforms.validators.number_range(0)])
    user_rfid = wtforms.IntegerField('Bruker RFID ', validators=[wtforms.validators.DataRequired()])


@app.route("/lend_book/", methods=['GET', 'POST'])
def lend_book():
    form = FormLendBook()
    if form.validate_on_submit():
        try:
            book.lend_book_rfid(flask.request.form["book_rfid"], flask.request.form["user_rfid"])
            flask.flash("Bok lånt!")
        except ConnectionError as err:
            return flask.render_template('user/error.html', error=err)
        flask.redirect(flask.url_for('lend_book'))

    return flask.render_template('user/lend_book.html', form=form)


@app.route('/user/<username>')
def show_user_profile(username):
    try:
        user_ = user.read_user_from_database(username)
    except ConnectionError as err:
        return flask.render_template('user/error.html', error=err)

    books_ = user.retrive_lended_books_by_user(username)

    return flask.render_template('user/user_profile.html', username=user_.username,
                                 rfid=user_.rfid, **user_.details, books=books_["books"])


@app.route('/admin/')
def admin_login():
    return flask.render_template('admin/login.html')


@app.route("/login_admin/", methods=['GET', 'POST'])
def login_admin():
    if flask.request.form:
        try:

            admin.admin_login(flask.request.form["user"], flask.request.form["pass"])

        except ConnectionError as err:
            # TODO Move error.html outside of user
            return flask.render_template('user/error.html', error=err)

        return flask.redirect(flask.url_for('admin_book'))

    return flask.render_template('admin/books_in_database.html')


@app.route('/admin/book/')
def admin_book():
    try:
        admin_ = admin.admin_fetch_all_books("109342903234")
    except ConnectionError as err:
        return flask.render_template('user/error.html', error=err)

    return flask.render_template('admin/books_in_database.html', books=admin_["books"])


@app.route('/admin/lent_books/')
def admin_lent_books():
    try:
        admin_ = admin.admin_get_lent_books("109342903234")
    except ConnectionError as err:
        return flask.render_template('user/error.html', error=err)

    return flask.render_template('admin/lent_books.html', history=admin_["history"])


@app.route('/admin/users_in_database/')
def admin_users_in_database():
    try:
        admin_ = admin.admin_get_users("109342903234")
    except ConnectionError as err:
        return flask.render_template('user/error.html', error=err)

    print(admin_)
    return flask.render_template('admin/users_in_database.html', users=admin_["users"])


if __name__ == "__main__":
    app.run(debug=True)
    '''
    Use this if you want other people on the same network access the web-page too
    app.run(host='0.0.0.0', debug=True)
    '''
