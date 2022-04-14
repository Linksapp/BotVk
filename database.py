import os.path
import sqlite3 as sql
from typing import List
from config import base_name

# изменить файловую структуру, сделать __init__.py

def sql_(func):
    def sql_execute():
        # ----
        func()
        # ----
    return sql_execute


"""
Запись истории в дб будет осуществлена следующим образомЖ
'/menu/menu2/photo' чтобы отслеживать перемешение пользователя по клавиатурам
"""



class DataBase:
    def __init__(self):
        self.base_name = base_name
        self.connector = None
        self.cursor = None


        if os.path.isfile(self.base_name): print(f'\033[32m Инициализация файла {self.base_name} прошла успешно! \033[37m')
        else: print(f'\033[33m Файл {self.base_name} был заново создан, инициализация прошла успешно! \033[37m')

        with sql.connect(f'{base_name}') as self.connector:
            self.cursor = self.connector.execute("""CREATE TABLE IF NOT EXISTS users(
                id           INT DEFAULT 0,
                first_name   VARCHAR,
                last_name    VARCHAR,
                history      VARCHAR,
                registration BOOLEAN DEFAULT 0
                )""")

            self.connector.commit()


    def get_info(self, *args, **kwargs) -> dict: 
        # доделать позже, сделать *args **kwargs
        self.cursor.execute(f""" SELECT {args} FROM users WHERE  """)

    def get_history(self, id: int, short: bool = False) -> str:
        self.cursor.execute(""" SELECT history FROM users WHERE id == ? """, (id,))

        if short == False: return self.cursor.fetchone()[0]
        else:
            catalog: str = self.cursor.fetchone()[0]
            return catalog[catalog.rfind('/'):]

    def change_history(self, id: int, catalog: str = '', flag: bool = True) -> None:
        
        if flag: catalog = self.get_history(id) + catalog
        else:
            catalog = self.get_history(id)
            if catalog.rfind('/') == 0: pass
            else: catalog = catalog[: catalog.rfind('/')]

        self.cursor.execute(""" UPDATE users SET history = ? WHERE id == ? """, (catalog, id))
        self.connector.commit()

    def save_info(self, user_info: dict, catalog: str = '/start') -> None:
        """ сохраняет информацию в бaзу данных """
        if user_info != {}:
            self.cursor.execute(""" SELECT id FROM users WHERE id == ? """, (user_info["id"],))
            _one = self.cursor.fetchone()
            if _one == None or user_info["id"] not in _one: 
                self.cursor.execute(""" INSERT INTO users(id, first_name, last_name, history, registration) VALUES(?, ?, ?, ?, ?)""", (user_info["id"], user_info["first_name"], user_info["last_name"], catalog, True))
                self.connector.commit()
                del _one


    def check_info(self) -> bool: pass