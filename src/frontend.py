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

forbiddenNames = ["søren klype"]

@app.route("/")
def welcome():
    return flask.render_template('user/startscreen/welcome.html')

@app.route("/create/", methods=['GET', 'POST'])
def create_user():
    if flask.request.form:
        #Check if username is too edgy
        if flask.request.form["fornavn"] in forbiddenNames:
            return flask.render_template('user_old/error.html', error="Et slikt navn er ikke lov!")

        user_ = user.User(**flask.request.form)

        try:
            user_.create_in_database()
        except ConnectionError as err:
            return flask.render_template('user_old/error.html', error=err)

        flask.flash("Bruker med navn {} og RFID {} opprettet".format(user_.username, user_.rfid))
        return flask.redirect(flask.url_for('create_user'))

    return flask.render_template('user/create user_old/lag_brukerinfo.html')

@app.route("/create/scan/")
def create_scan():
    return flask.render_template('user/create user_old/create_scanrfid.html')

@app.route("/create/chooserfid/")
def create_setrfid():
    return flask.render_template('user/create user_old/lag_pin.html')

@app.route("/create/confirmrfid/")
def create_confirmrfid():
    return flask.render_template('user/create user_old/confirm_pin.html')

@app.route("/create/creationvalid/")
def create_sucsess():
    return flask.render_template('user/create user_old/lagd_bruker.html')

@app.route("/create/rules/")
def create_rules():
    return flask.render_template('user/create user_old/regler.html')

#Ask the user_old if she wants an adult to confirm the account registration now or not
@app.route("/create/adultconfirm/")
def create_adult_confirm():
    return flask.render_template('user/create user_old/voksengodkjennelse.html')

@app.route("/create/adultconfirmcheckbox/")
def create_adult_confirm_checkbox():
    return flask.render_template('user/create user_old/voksengodkjennelsen.html')

@app.route("/start/")
def startscreen():
    return flask.render_template('user/startscreen/start.html')










@app.route("/profile/my_recomendations/")
def my__recomendations():
    return flask.render_template('user/login_profile/login_anmeldelser.html')

@app.route("/profile/history/")
def profile_history():
    return flask.render_template('user/login_profile/login_lan.html')

@app.route("/profile/menu/")
def profile_menu():
    return flask.render_template('user/login_profile/login_main.html')

@app.route("/profile/pin/")
def profile_pin():
    return flask.render_template('user/login_profile/login_pin.html')

@app.route("/profile/scanRFID/")
def profile_scanRFID():
    return flask.render_template('user/login_profile/login_scan.html')

@app.route("/profile/change_info/")
def profile_change_info():
    return flask.render_template('user/login_profile/login_profil.html')








@app.route("/lend/wrongpin/")
def lend_wrong_pin():
    return flask.render_template('user/lend_book/lan_feil_pin.html')

@app.route("/lend/enterpin/")
def lend_enterpin():
    return flask.render_template('user/lend_book/lan_skriv_pin.html')

@app.route("/lend/scan/")
def lend_scan():
    return flask.render_template('user/lend_book/lan_scan.html')

@app.route("/lend/verified/")
def lend_verified():
    return flask.render_template('user/lend_book/lan_godkjent.html')

@app.route("/lend/search/")
def lend_search():
    return flask.render_template('user/lend_book/finn_sok.html')

@app.route("/lend/searchresults/")
def lend_searchresults():
    return flask.render_template('user/lend_book/finn_resultater.html')

@app.route("/lend/bookinfo/")
def lend_bookinfo():
    return flask.render_template('user/lend_book/bok_info.html')




@app.route("/deliver/category/")
def deliver_category():
    return flask.render_template('user/deliver_book/bok_kategori.html')

@app.route("/deliver/ratecomment/")
def deliver_ratecomment():
    return flask.render_template('user/deliver_book/bok_kommentar.html')

@app.route("/deliver/delivered")
def deliver_delivered():
    return flask.render_template('user/deliver_book/bok_levert.html')

@app.route("/deliver/scan")
def deliver_scan():
    return flask.render_template('user/deliver_book/levere_scan.html')

"""
@app.route("/create/", methods=['GET', 'POST'])
def create_user():
    if flask.request.form:
        #Check if username is too edgy
        if flask.request.form["username"] in forbiddenNames:
            return flask.render_template('user_old/error.html', error="Et slikt navn er ikke lov!")

        user_ = user_old.User(**flask.request.form)

        try:
            user_.create_in_database()
        except ConnectionError as err:
            return flask.render_template('user_old/error.html', error=err)

        flask.flash("Bruker med navn {} og RFID {} opprettet".format(user_.username, user_.rfid))
        return flask.redirect(flask.url_for('create_user'))

    return flask.render_template('user_old/create_user.html')


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
            return flask.render_template('user_old/error.html', error=err)
        flask.redirect(flask.url_for('lend_book'))

    return flask.render_template('user_old/lend_book.html', form=form)


@app.route('/user_old/<username>')
def show_user_profile(username):
    try:
        user_ = user_old.read_user_from_database(username)

    except ConnectionError as err:
        return flask.render_template('user_old/error.html', error=err)

    books_ = user_old.retrive_lended_books_by_user(username)

    return flask.render_template('user_old/user_profile.html', username=user_.username, rfid=user_.rfid, details= user_.details, books=books_["books"])


@app.route('/admin/')
def admin_login():
    return flask.render_template('admin/login.html')


@app.route("/login_admin/", methods=['GET', 'POST'])
def login_admin():
    if flask.request.form:
        try:

            admin.admin_login(flask.request.form["user_old"], flask.request.form["pass"])

        except ConnectionError as err:
            # TODO Move error.html outside of user_old
            return flask.render_template('user_old/error.html', error=err)

        return flask.redirect(flask.url_for('admin_book'))

    return flask.render_template('admin/books_in_database.html')


@app.route('/admin/book/')
def admin_book():
    try:
        admin_ = admin.admin_fetch_all_books("109342903234")
    except ConnectionError as err:
        return flask.render_template('user_old/error.html', error=err)

    return flask.render_template('admin/books_in_database.html', books=admin_["books"])


@app.route('/admin/lent_books/')
def admin_lent_books():
    try:
        admin_ = admin.admin_get_lent_books("109342903234")
    except ConnectionError as err:
        return flask.render_template('user_old/error.html', error=err)

    return flask.render_template('admin/lent_books.html', history=admin_["history"])


@app.route('/admin/users_in_database/')
def admin_users_in_database():
    try:
        admin_ = admin.admin_get_users("109342903234")
    except ConnectionError as err:
        return flask.render_template('user_old/error.html', error=err)


    return flask.render_template('admin/users_in_database.html', users=admin_["users"])
"""

if __name__ == "__main__":
    app.run(debug=True)
    '''
    Use this if you want other people on the same network access the web-page too
    app.run(host='0.0.0.0', debug=True)
    '''
