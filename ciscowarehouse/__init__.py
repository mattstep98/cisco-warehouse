import json
import os
from flask import Flask, render_template,session,redirect,url_for,g
from flask_mysqldb import MySQL
from . import auth
import functools

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    #Configuration file
    with open('config.json') as config_file:
        config_data = json.load(config_file)
   
    # database configuration from config file
    db_settings = config_data['database']
    app.config.update(db_settings)

    mysql = MySQL(app)



    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))

            return view(**kwargs)

        return wrapped_view



    #A simple page that says hello
    @app.route('/hello')
    @login_required
    def hello():
        return render_template('hello.html', title='HELLO', username=session.get('username'))

    @app.route('/database')
    def database():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM ciscowarehouse.user;")
        response = cursor.fetchall()
        cursor.close()
        return str(response)


    from . import auth
    app.register_blueprint(auth.bp)


    return app
