import json

base = 'dumb_db.txt'

def get_info() -> dict:
    pass

def save_info(user_info: dict) -> bool:
    with open(base, 'a', encoding='UTF-8') as file:
        file.write(str(user_info) + '\n')
        return True

def read_info(user_info: dict) -> bool:
    try:
        with open(base, 'r', encoding='UTF-8') as file:
            for i in file.readlines(): 
                if str(user_info) in i: return True
        return False
    except FileNotFoundError as error: 
        with open(base, 'w', encoding='UTF-8') as file:
            file.write(str(user_info) + '\n')
        return True

