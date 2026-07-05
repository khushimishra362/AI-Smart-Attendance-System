import sqlite3
import os
def create_database():

    conn = sqlite3.connect("attendance.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            date TEXT,

            time TEXT

        )
    """)

    conn.commit()

    conn.close()

def connect_db():
    print(os.path.abspath("attendance.db"))
    conn = sqlite3.connect("attendance.db")
    return conn


def create_table():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close() 

def get_attandance():
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    data=cursor.fetchall()
    conn.close()
    return data
