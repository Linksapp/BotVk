import sqlite3 as sql
import os.path

def a():
    with sql.connect('data_base.db') as connector:
        cursor = connector.cursor()

        cursor.execute("""SELECT 'last_name'  FROM sqlite_master WHERE type='table' AND name='users' """)

        if cursor.fetchone()[0] == 1:
            print(True, cursor.fetchone()[0])
        else: print(0, cursor.fetchone())

    
if os.path.isfile('data_base.db'): print( True)
con = sql.connect('data_base.db')
c = con.cursor()

inf = c.execute(""" SELECT id FROM users WHERE id==?""", (376919311,))


for i in inf:
    if 376919311 in i:
        print(1)