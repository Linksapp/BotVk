import sqlite3 as sql
from config import base_name

# изменить файловую структуру, сделать __init__.py
# close()

def init() -> bool: 
    global connector, cursor
    try:
        connector = sql.connect(f'{base_name}')
        cursor = connector.execute("""CREATE TABLE IF NOT EXISTS users(
            count INT PRIMARY KEY,
            id INT,
            first_name VARCHAR,
            last_name VARCHAR,
        )""")
        print(f'\033[32m Инициализация файла {base_name} прошла успешно! \033[37m')
        return True
    except Exception as error:
        print(f'\033[31m{error}\033[37m')
        return False


def get_info(id: int = None, first_name: str = None, last_name: str = None) -> dict: 
    # доделать позже, сделать *args **kwargs
    cursor.execute("""SELECT first_name FROM users WHERE last_name == 'Дрожжев' """)


def save_info(user_info: dict) -> bool:
    try:
        cursor.execute(f"""INSERT INTO users(id, first_name, last_name) VALUES(?, ?, ?)""", [user_info["id"], user_info["first_name"], user_info["last_name"]])
        connector.commit()
        return True
    except Exception as error:
        return False

def check_info() -> bool: pass