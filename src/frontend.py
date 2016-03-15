import random
import book
import flask
import user

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'temmelighemmelig'

forbiddenNames = ["søren klype"]
pincode = 0

#Lend and deliver book stations
@app.route("/scan_book/", methods=['GET', 'POST'])
def scan_book():
    ids = 0
    if flask.request.form:

        #Gets the user rfid and book rfid or just the book rfid from JS rfid scanning script
        ids = flask.request.form["text_rfid"].replace('\x00', '')

        try:
            #Sends the rfids to backend trough the API
            global book_
            book_ = book.scan_book(ids)
            print(book_)

        except ConnectionError as err:
            #Displays an error page with an error if something went wrong, e.g. the book is not registered
            return flask.render_template('user/scanning_station/lane_levere_feil.html', error=err, rfid_targetfunction="scan_book")

        if book_["type"] == "lend":
            return flask.render_template('user/scanning_station/lane_levere_lant.html', rfid_targetfunction="scan_book", status=book_["status"], name=book_["username"])

        elif book_["type"] == "deliver":
            return flask.render_template('user/scanning_station/lane_levere_levert.html', rfid_targetfunction="scan_book", status=book_["status"], name=book_["username"])

    return flask.render_template('user/scanning_station/lane_levere_forside.html', ids=ids, rfid_targetfunction="scan_book")

@app.route("/putback/")
def putbookback():

    return flask.render_template('user/scanning_station/lane_levere_sett_pa_plass.html', status=book_["status"])

@app.route("/rfidtest/", methods=['GET', 'POST'])
def rfid():
    ids = 0
    if flask.request.form:
        ids = flask.request.form["text_rfid"].replace('\x00', '')



    return flask.render_template('user/index.html', ids=ids)

@app.route("/")
def welcome():
    return flask.render_template('user/startscreen/welcome.html')

@app.route("/start/")
def start():
    return flask.render_template('user/startscreen/startmenu.html')

@app.route("/create/", methods=['GET', 'POST'])
def create_user():
    if flask.request.form:
        print(flask.request.form)
        #Check if username is too edgy
        if flask.request.form["username"] in forbiddenNames:
            return flask.render_template('user_old/error.html', error="Et slikt navn er ikke lov!")

        user_ = user.User(rfid=random.randrange(1,1000000), **flask.request.form)




        try:
            user_.create_in_database()
        except ConnectionError as err:
            return flask.render_template('user_old/error.html', error=err)

        flask.flash("Bruker med navn {} og RFID {} opprettet".format(user_.username, user_.rfid))
        return flask.render_template('user/create_user/assign_user_rfid.html')

    return flask.render_template('user/create_user/enter_user_info.html')

@app.route("/create/setrfid/", methods=['GET', 'POST'])
def scanrfid():
    ids = 0
    if flask.request.form:
        ids = flask.request.form["text_rfid"]
        ids = ids.split(";")



    return flask.render_template('user/create_user/assign_user_rfid.html')


@app.route("/create/scan/", methods=['GET', 'POST'])
def create_scan():

    if flask.request.form:
        rfid = flask.request.form["rfid"]

    return flask.render_template('user/create_user/enter_pin.html')


@app.route("/create/choosepin/", methods=['GET', 'POST'])
def create_setpin():
    if flask.request.form:
        pincode = flask.request.form["pin1"] + flask.request.form["pin2"] + flask.request.form["pin3"] + flask.request.form["pin4"]
        confirmPincode = flask.request.form["confirm_pin1"] + flask.request.form["confirm_pin2"] + flask.request.form["confirm_pin2"] + flask.request.form["confirm_pin2"]

        if pincode == confirmPincode:
            pin_ = user.set_user_pincode(str(pincode), "1")
            return flask.render_template('user/create_user/adult_confirmation_yORn.html')
        else:
            print("Pinkodene samsvarer ikke")

    return flask.render_template('user/create_user/enter_pin.html')

"""
@app.route("/create/confirmpin/", methods=['GET', 'POST'])
def create_confirmrfid():
    if flask.request.form:
        confirm_pincode = flask.request.form["pin1"] + flask.request.form["pin2"] + flask.request.form["pin3"] + flask.request.form["pin4"]
        print("Pincode is " +  str(pincode))
        print("Confirmed pincode is " + confirm_pincode)

        if pincode == confirm_pincode:
            print("Pincodes are the same")
    return flask.render_template('user/create_user/confirm_pin.html')
"""


@app.route("/login/")
def login():
    try:
        user_ = user.login_user("1")

        global sessionID
        sessionID = user_["sessionID"]
        print("User logged in")

        return flask.redirect(flask.url_for('profile_menu'))

    except ConnectionError as err:
        return flask.render_template('user_old/error.html', error=err)


    userRFID = "1"
    if userRFID == 1:
        return flask.render_template('user/login_profile/login_pin.html')


    return flask.render_template('user/login_profile/login_scan.html')

@app.route("/login/pincode/", methods=['GET', 'POST'])
def login_pin():
    if flask.request.form:

        pincode = flask.request.form["pin1"] + flask.request.form["pin2"] + flask.request.form["pin3"] + flask.request.form["pin4"]

        # FIXME - Get the userRFID from "/login/"
        userRFID = "1"

        #If the login is correct, the user will be sent to the profile menu screen
        try:
            user_ = user.login_user(userRFID)

            global sessionID
            sessionID = user_["sess_id"]
            print("User logged in")

            return flask.redirect(flask.url_for('profile_menu'))

        except ConnectionError as err:
            return flask.render_template('user_old/error.html', error=err)


    return flask.render_template('user/login_profile/login_pin.html')

@app.route("/profile/menu/")
def profile_menu():
    try:
        print("SessionID is ", sessionID)
        usr = user.read_user_from_database(sessionID)

    except ConnectionError as err:
        return flask.render_template('user_old/error.html', error=err)

    return flask.render_template('user/login_profile/profile_menu.html', username=usr["username"])


@app.route("/profile/history/")
def lent_books_history():
    try:
        print("SessionID is ", sessionID)
        usr = user.retrive_lended_books_by_user(sessionID)

        return flask.render_template('user/login_profile/login_lan.html', books=usr["books"])
    except ConnectionError as err:
        return flask.render_template('user_old/error.html', error=err)

    return flask.render_template('user/login_profile/profile_menu.html')


@app.route("/profile/change_info/")
def profile_info():
    try:
        print("SessionID is ", sessionID)
        usr = user.read_user_from_database(sessionID)
        print(usr)
        return flask.render_template('user/login_profile/profile_info.html', userinfo=usr)
    except ConnectionError as err:
        return flask.render_template('user_old/error.html', error=err)

    return flask.render_template('user/login_profile/profile_info.html')

"""
@app.route("/create/creationvalid/")
def create_sucsess():
    return flask.render_template('user/create user/lagd_bruker.html')

@app.route("/create/rules/")
def create_rules():
    return flask.render_template('user/create user/rules.html')

#Ask the user if she wants an adult to confirm the account registration now or not
@app.route("/create/adultconfirm/")
def create_adult_confirm():
    return flask.render_template('user/create user/adult_confirmation_yORn.html')

@app.route("/create/adultconfirmcheckbox/")
def create_adult_confirm_checkbox():
    return flask.render_template('user/create user/adult_confirmation_checkboxes.html')

@app.route("/start/")
def startscreen():
    return flask.render_template('user/startscreen/startmenu.html')


@app.route("/profile/my_recomendations/")
def my__recomendations():
    return flask.render_template('user/login_profile/login_anmeldelser.html')

@app.route("/profile/history/")
def profile_history():
    return flask.render_template('user/login_profile/login_lan.html')



@app.route("/profile/pin/")
def profile_pin():
    return flask.render_template('user/login_profile/login_pin.html')

@app.route("/profile/scanRFID/")
def profile_scanRFID():
    return flask.render_template('user/login_profile/login_scan.html')

@app.route("/profile/change_info/")
def profile_change_info():
    return flask.render_template('user/login_profile/profile_menu.html')








@app.route("/lend/wrongpin/")
def lend_wrong_pin():
    return flask.render_template('user/lend_book/lend_wrong_pin.html')

@app.route("/lend/enterpin/")
def lend_enterpin():
    return flask.render_template('user/lend_book/lend_enter_pincode.html')

@app.route("/lend/scan/")
def lend_scan():
    return flask.render_template('user/lend_book/scan_book.html')

@app.route("/lend/verified/")
def lend_verified():
    return flask.render_template('user/lend_book/scan_succsess.html')

@app.route("/lend/search/")
def lend_search():
    return flask.render_template('user/lend_book/search_book.html')

@app.route("/lend/searchresults/")
def lend_searchresults():
    return flask.render_template('user/lend_book/list_books.html')

@app.route("/lend/bookinfo/")
def lend_bookinfo():
    return flask.render_template('user/lend_book/book_info.html')




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
"""
@app.route("/create/", methods=['GET', 'POST'])
def create_user():
    if flask.request.form:
        #Check if username is too edgy
        if flask.request.form["username"] in forbiddenNames:
            return flask.render_template('user/error.html', error="Et slikt navn er ikke lov!")

        user_ = user.User(**flask.request.form)

        try:
            user_.create_in_database()
        except ConnectionError as err:
            return flask.render_template('user/error.html', error=err)

        flask.flash("Bruker med navn {} og RFID {} opprettet".format(user_.username, user_.rfid))
        return flask.redirect(flask.url_for('create_user'))

    return flask.render_template('user/create_user.html')


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

    return flask.render_template('user/user_profile.html', username=user_.username, rfid=user_.rfid, details= user_.details, books=books_["books"])


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


    return flask.render_template('admin/users_in_database.html', users=admin_["users"])
"""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    '''
    Use this if you want other people on the same network access the web-page too
    app.run(host='0.0.0.0', debug=True)
    '''
