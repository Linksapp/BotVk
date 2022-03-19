from email.mime import base
import json
from config import base_name

# json не подходит для хранения данных, нагружает память при записи из-за того что нельзя дополнять его
# либо хранить данные в json без сортировки
a = {'users': []}


def init_json() -> bool:
    try:
        with open(base_name, 'r') as file:
            json.load(file)
            print(f'{base_name.upper()} Успешно инициализированна')
            return True
    except FileNotFoundError:
        with open(base_name, 'w') as file:
            json.dump(a, file, indent=2)
            print(f'Файл {base_name.upper()} был заного создан')
            return True
    except Exception as error: 
        print(error)
        return False

def get_info(id: int) -> dict | None:
    data: list = read_json()
    with open(base_name, 'r') as file:
        for _ in data:
            if id == _['id']: return _
            else: return None

def save_info(user_info: dict = None) -> bool:
    data: list = read_json()
    with open(base_name, 'w') as file:
        if user_info in data:
            a['users'] = data
            json.dump(a, file, indent=2)
            return True
        elif user_info not in data: 
            data.append(user_info)
            a['users'] = data
            json.dump(a, file, indent=2)
            return True

def read_info(user_info: dict = None) -> bool:
    data: list = read_json()
    with open(base_name, 'r') as file:
        for _ in data:
            if user_info == _: return True
            else: return False


def read_json() -> list:
    with open(base_name, 'r') as file:
        #print(json.load(file)['users'])
        return json.load(file)['users']
