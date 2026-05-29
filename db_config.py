import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="080512",
            database="ethical_ai"
        )
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        raise
