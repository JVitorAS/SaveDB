import mysql.connector

def connect():
    db = "STEAM"
    host = "localhost"
    user = "root"
    password = ""

    conn = mysql.connector.connect(host=host, user=user, password=password, database=db)
    return conn