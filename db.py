import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="RMSBCA16",
        database="quiz_system"
    )