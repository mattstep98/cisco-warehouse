from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import json


with open('config.json') as config_file:
    config_data = json.load(config_file)
mydb = mysql.connector.connect(host=config_data['database']['MYSQL_HOST'], user=config_data['database']['MYSQL_USER'],password=config_data['database']['MYSQL_PASSWORD'],database=config_data['database']['MYSQL_DB'])
print(mydb)
mycursor = mydb.cursor(buffered=True)

bp = Blueprint('zones', __name__, url_prefix='/home')

@bp.route('/zones')
def zones():
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))
    else:
        mycursor.execute("SELECT * FROM inventory ORDER BY zone asc;")
        inventory = mycursor.fetchall()


        return render_template('zones.html',title='Zones',username=session.get('username'),inventoryByZoneAsc=inventory)