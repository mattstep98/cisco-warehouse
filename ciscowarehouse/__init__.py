import os
from flask import Flask
from flask_mysqldb import MySQL
import json


def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    #Configuration file
    with open('config.json') as config_file:
        config_data = json.load(config_file)
   
    # database configuration from config file
    db_settings = config_data['database']
    app.config.update(db_settings)

    mysql = MySQL(app)

    #A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'

    @app.route('/database')
    def database():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM ciscowarehouse.inventory;")
        response = cursor.fetchall()
        cursor.close()
        return str(response)

    return app
