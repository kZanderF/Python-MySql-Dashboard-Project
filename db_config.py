import MySQLdb

def db_connection():
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='Kd.128987550',
        db='sales_dashboard'
    )
    return conn
