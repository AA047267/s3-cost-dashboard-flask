from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'QAZplm123!!!'
app.config['MYSQL_DB'] = 's3_bucket'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')


@app.route('/all_buckets/')
def all_buckets():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM s3_bucket_size")
    rows = cur.fetchall()
    return render_template('all_buckets.html', rows = rows)
    cur.close()

@app.route('/dm')
def dm_buckets():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM dm_bucket_size")
    rows = cur.fetchall()
    return render_template('dm_buckets.html', rows = rows)
    cur.close()

@app.route("/fetch_bucket", methods=["GET", "POST"])
def fetch_bucket_info():
    if request.method == "POST":
        name = request.form["name"]
        print(name)
        cur = mysql.connection.cursor()
        fetch = cur.execute("SELECT * FROM s3_bucket_size WHERE name = %s", [name])
        one_bucket = cur.fetchone()
        return render_template("bucket_search.html", one_bucket=one_bucket) 

@app.route("/fetch_dm_bucket", methods=["GET", "POST"])
def fetch_dm_bucket_info():
    if request.method == "POST":
        name = request.form["name"]
        print(name)
        cur = mysql.connection.cursor()
        fetch = cur.execute("SELECT * FROM dm_bucket_size WHERE name = %s", [name])
        one_bucket = cur.fetchone()
        return render_template("bucket_search.html", one_bucket=one_bucket) 
    

if __name__ == '__main__':
    app.run(debug=True)
