import sqlite3
from flask import g,Flask,render_template,request
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

def getIndexPage(tableName):
    columnNames = query_db(f"SELECT t.name FROM pragma_table_info('{tableName}') t")
    data = query_db(f"SELECT * FROM {tableName};")
    if len(data)>0:
        columns = len(data[0])
    else:
        columns = 0
    return render_template("index.html",data=data,columns=columns,columnNames=columnNames)

def updateTable(tableName,records):
    sql1 = f'DELETE FROM {tableName}'
    query_db(sql1)

    for record in records:
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = f'INSERT INTO {tableName} VALUES({columns})'
        query_db(sql2,record)
    get_db().commit()


@app.route("/tableUpdate",methods=["POST"])
def tableUpdate():
    data = request.get_json()
    if data is None:
        pass
    else:
        updateTable("test2",data)
    return ("nothing")

@app.route("/test")
def test():
    print("testfunction")

@app.route('/',methods=["GET","POST"])
def index():
    tableName = "test2"
    return getIndexPage(tableName)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == "__main__":      #runs the application
    app.run()     #debug allows us to not have to refresh every time
