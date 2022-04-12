import time
import sqlite3 as sql
from config import base_name

def main(func):
    def a(one_time=False):
        print(0)
        func(one_time)
        print(0)
        return []
    return a

@main
def c(c = None): print(c)

main_menu = {
		'Красная': 'negative', 
		'Зеленая': 'positive', 
		'Синяя': 'primary', 
		'Белая': 'secondary', 
		'': None,
		'Меню 2': 'secondary'
	}

history = '/menu/menu2/photo'
"""history = history[: history.rfind('/')]
history = history[: history.rfind('/')]
print(history[: history.rfind('/')])"""


def change():
	id = 376919311

	with sql.connect(base_name) as file:
		cursor = file.execute("""CREATE TABLE IF NOT EXISTS users(
                id           INT DEFAULT 0,
                first_name   VARCHAR,
                last_name    VARCHAR,
                history      VARCHAR,
                registration BOOLEAN DEFAULT 0
                )""")
		
		cursor.execute(""" SELECT history FROM users WHERE id == ? """, (id,))
		
		_catalog: str = cursor.fetchone()[0]
		_catalog = _catalog[: _catalog.rfind('/')]

		cursor.execute(""" UPDATE users SET history = ? WHERE id == ? """, (_catalog, id))
		
		file.commit()

change()