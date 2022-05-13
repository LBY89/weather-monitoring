import psycopg2 #this is the driver connect to database, flask connecting postgresql
def createConnection():
    return psycopg2.connect(dbname='smart_db', user='smart',
    host='db', password='smart')

