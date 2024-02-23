import sqlite3

conn = sqlite3.connect("cmt.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE cmt (
    id integer PRIMARY KEY,
    cmt text NOT NULL,
    predict text NOT NULL
) """
cursor.execute(sql_query)