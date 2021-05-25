import sqlite3
from flask import g,Flask,render_template,request
from os import path
DATABASE = 'flaskTest.db'
fileDir = path.dirname(__file__) # for loading images
currentTableName = None

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

def getIndexPage(tableName,tableData = None):
    columnNames = query_db(f"SELECT t.name FROM pragma_table_info('{tableName}') t")
    # print(columnNames)
    if tableData is None:
        data = query_db(f"SELECT * FROM {tableName};")
    else:
        data = tableData
    if len(data)>0:
        columns = len(data[0])
    else:
        columns = 0
    tables = query_db("SELECT name FROM sqlite_master WHERE type='table' AND NOT (name = 'sqlite_sequence' OR name='Current');")
    return render_template("index.html",data=data,columns=columns,columnNames=columnNames,tables=tables)

def updateTable(tableName,records):
    sql1 = f'DELETE FROM {tableName}'
    query_db(sql1)

    for record in records:
        # print(record)
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
        updateTable("Current",data)
        global currentTableName
        if currentTableName is None:
            print("Data is not being saved")
        else:
            updateTable(currentTableName,data)
    return ("nothing")

def searchSQLTable(tableName,columnName,searchValue):
    sql1 =f"SELECT * FROM {tableName} WHERE {columnName} = '{searchValue}'"
    data = query_db(sql1)
    return data

@app.route("/searchTable",methods=["POST"])
def searchTable():
    tableName = "Current"
    data = request.get_json()
    if data is None:
        return ("nothing")
    else:
        # print(data)
        # print(data["columnName"])
        tableData = searchSQLTable(tableName,data["columnName"],data["searchValue"])
        # print(tableData)
        createCurrentTableFromSearch(tableData)
        # print(tableData)
        # return getIndexPage(tableName,tableData=tableData)
        return ("nothing")

@app.route("/test")
def test():
    print("testfunction")

def createCurrentTableFromSearch(tableData):
    sql1 = 'DELETE FROM Current;'
    query_db(sql1)
    for record in tableData:
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = f'INSERT INTO "Current" VALUES({columns})'
        query_db(sql2,record)
    get_db().commit()
    if len(query_db("SELECT * FROM Current")) == 0:
        print("There are no rows that fit that criteria")

def createCurrentTable(tableName):
    columnNames = query_db(f"SELECT t.name FROM pragma_table_info('{tableName}') t")
    columnInformation = ""
    for column in columnNames:
        columnInformation = columnInformation + f"{column[0]} TEXT NOT NULL,"
    columnInformation = columnInformation[0:len(columnInformation)-1]
    # print(columnInformation)
    data = query_db(f"SELECT * FROM {tableName};")
    query_db("DROP TABLE IF EXISTS Current")
    query_db(f"CREATE TABLE 'Current' ({columnInformation})")
    for record in data:
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = f'INSERT INTO "Current" VALUES({columns})'
        query_db(sql2,record)
    get_db().commit()

def createCurrentTableFromData(data):
    # print(data)
    columnNames = list(data[0].keys())
    # print(columnNames)
    columnInformation = ""
    for column in columnNames:
        columnInformation = columnInformation + f"{column} TEXT NOT NULL,"
    columnInformation = columnInformation[0:len(columnInformation)-1]
    # print(columnInformation)
    query_db("DROP TABLE IF EXISTS Current")
    query_db(f"CREATE TABLE 'Current' ({columnInformation})")
    for record in data:
        record = list(record.values())
        # print(record)
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql2 = f'INSERT INTO "Current" VALUES({columns})'
        # print(sql2)
        query_db(sql2,record)
    get_db().commit()


@app.route('/openTable',methods=["POST"])
def openTable():
    tableName = request.get_json()
    if tableName is None:
        return ("nothing")
    else:
        global currentTableName
        currentTableName = tableName
        createCurrentTable(tableName)
    return("nothing")

# global currentTableName
@app.route('/',methods=["GET","POST"])
def index():
    # createCurrentTable(currentTableName)
    if not checkIfTableExisits("Current"):
        global currentTableName
        createCurrentTable(currentTableName)
    return getIndexPage("Current")


@app.route('/openExcelFile',methods=["POST"])
def openExcelFile():
    data = request.get_json()
    if data is None:
        return ("nothing")
    else:
        createCurrentTableFromData(data)
        global currentTableName
        currentTableName = None
        # print(data)
    # index()
    return ("nothing")


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def checkIfTableExisits(tableName):  #returns true or false if exisits or not

    results = query_db(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{tableName}";')
    if len(results)==1:
        return True
    else:
        return False

if __name__ == "__main__":      #runs the application
    app.run()     #debug allows us to not have to refresh every time
