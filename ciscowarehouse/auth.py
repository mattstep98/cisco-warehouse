from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import json


with open('config.json') as config_file:
        config_data = json.load(config_file)
mydb = mysql.connector.connect(host=config_data['database']['MYSQL_HOST'], user=config_data['database']['MYSQL_USER'],password=config_data['database']['MYSQL_PASSWORD'],database=config_data['database']['MYSQL_DB'])
print(mydb)
mycursor = mydb.cursor(buffered=True)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                print("trying")
                mycursor.execute(
                    "INSERT INTO user (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password)),
                )
                mydb.commit()
            except:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        #mycursor.execute(("SELECT * FROM user WHERE username = '"+username+"';"))#, (username))
        mycursor.execute("SELECT * FROM user WHERE user.username = '{}';".format(username))
        user = mycursor.fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home.home'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        mycursor.execute('SELECT * FROM user WHERE id = {}'.format(user_id))
        g.user = mycursor.fetchone()
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.login'))

