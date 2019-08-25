from flask import Flask, render_template, request, redirect, url_for
from data import tag_data
from wtforms import Form, TextAreaField, StringField, IntegerField, validators
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_DB'] = 'jsse'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

cur = mysql.connection.cursor()
tags_data = tagcur.execute('SELCT tag_id from tags')
print(tags_data)

mysql.connection.commit()
cur.close()

if __name__ == "__main__":
    app.run(debug=True)