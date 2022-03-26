import sqlite3 as sql
import os.path

def a():
    with sql.connect('data_base.db') as connector:
        cursor = connector.cursor()

        cursor.execute("""SELECT 'last_name'  FROM sqlite_master WHERE type='table' AND name='users' """)

        if cursor.fetchone()[0] == 1:
            print(True, cursor.fetchone()[0])
        else: print(0, cursor.fetchone())


con = sql.connect('data_base.db')
c = con.cursor()

c = con.execute("""CREATE TABLE IF NOT EXISTS users (
                count       INT PRIMARY KEY NOT NULL,
                id          INT,
                first_name  VARCHAR,
                last_name   VARCHAR
                )""")

inf = c.execute(""" SELECT id FROM users WHERE id==?""", (376919311,))


print(c.fetchone() != None)
print(c.fetchone())
