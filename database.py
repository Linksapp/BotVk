import os.path
import sqlite3 as sql
from config import base_name

# изменить файловую структуру, сделать __init__.py

def init() -> bool: 
    global connector, cursor

    isTrue = True
    if os.path.isfile(base_name) == False: isTrue = False

    with sql.connect(f'{base_name}') as connector:
        cursor = connector.execute("""CREATE TABLE IF NOT EXISTS users (
                count INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                id INT,
                first_name VARCHAR,
                last_name VARCHAR
                )""")

    if isTrue == False: print(f'\033[33m Файл {base_name} был заново создан, инициализация прошла успешно! \033[37m')
    else: print(f'\033[32m Инициализация файла {base_name} прошла успешно! \033[37m')
    return True


def get_info(id: int = None, first_name: str = None, last_name: str = None) -> dict: 
    # доделать позже, сделать *args **kwargs
    cursor.execute("""SELECT first_name FROM users WHERE last_name == 'Дрожжев' """)


def save_info(user_info: dict) -> bool:
    cursor.execute("""SELECT id FROM users WHERE id == ? """, (user_info["id"],))
    if user_info["id"] not in cursor.fetchone(): 
        cursor.execute(f"""INSERT INTO users(id, first_name, last_name) VALUES(?, ?, ?)""", [user_info["id"], user_info["first_name"], user_info["last_name"]])
        connector.commit()
        return True
    else: return False

def check_info() -> bool: pass