import sqlite3
from sqlite3 import Error
from flask import session

DB_FILE = r"db\database.db"

def get_connection(immediate=False):
    conn = None
    try:
        db_file = DB_FILE
        if immediate:
            conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES,
                                            isolation_level="IMMEDIATE")
        else:
            conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    except Error as e:
        print(e)
    return conn

def get_connection_non_flask(is_debug):
    conn = None
    try:
        db_file = DB_FILE
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    except Error as e:
        print(e)
    return conn

def get_data(cur, query):
    cur.execute(query)
    column_names = [x[0] for x in cur.description]
    rows = cur.fetchall()
    return column_names, rows

def get_data_dict(cur, query):
    cur.execute(query)
    column_names = [x[0] for x in cur.description]
    temp_rows = cur.fetchall()
    rows = [dict(zip(column_names, row)) for row in temp_rows]
    return rows

if __name__ == '__main__':
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM PRINTERS")
    