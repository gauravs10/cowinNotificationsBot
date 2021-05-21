import psycopg2, keys, os

def createDB(primitiveInput):

    databaseURL = os.environ['DATABASE_URL']
    primitiveInput.postGresConn = psycopg2.connect(databaseURL, sslmode = 'require')
    primitiveInput.postGresDB = primitiveInput.postGresConn.cursor()
    try:
        primitiveInput.postGresDB.execute('CREATE TABLE IF NOT EXISTS cowin (id SERIAL, notification TEXT NOT NULL)')
    except:
        pass

def insertDbCommand(primitiveInput, statement):
    primitiveInput.postGresDB.execute('INSERT INTO cowin (notification) VALUES (%s);', [statement])

def selectDbCommand(primitiveInput, statement):
    primitiveInput.postGresDB.execute('SELECT notification FROM cowin where notification = %s', [statement])

def commitDBConn(primitiveInput):
    primitiveInput.postGresConn.commit()

def dbClose(primitiveInput):
    primitiveInput.postGresDB.close()