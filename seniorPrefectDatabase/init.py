import sqlite3
from flask import g,Flask,render_template
from os import path
DATABASE = 'flaskTest.db'
fileDir = path.dirname(__file__) # for loading images

app = Flask(__name__)   #creates the application flask
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext  #closes the database when the file is closed
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    cur = get_db().cursor()
    data = query_db("SELECT * FROM test;")
    return render_template("index.html",data=data)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == "__main__":      #runs the application
    app.run()     #debug allows us to not have to refresh every time
