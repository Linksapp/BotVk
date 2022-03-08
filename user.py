import json
#
class User:
    """Default User Class"""
    def __init__(self, user_info: dict, registration: bool = False) -> None:
        # Пользовательские данные
        if user_info == {}: self.create = False
        else:
            self.user_info = user_info
            self.registratiom = registration
            self.create = True

        self.return_error()
        self.save_info()
    
    def get_info(self):
        pass

    def save_info(self):
        """При записи нового пользователя, очищает бд. Фикс it"""
        with open('dumb_db.txt', 'w', encoding='UTF-8') as file:
            file.write(str(self.user_info) + '\n')
            return True
    
    def return_error(self): 
        if self.create == False: raise BaseException('Error! Dont get user_info like full dict')
        else: pass

    def check_create(self) -> bool:
        """Дописать функцию"""
        with open('dumb_db.txt', 'r', encoding='UTF-8') as file:
            if self.user_info in file:
                return True
            else:
                self.save_info() # передовать все необходимые аргументы для сохранения
                return True

    def print_info(self):
        print(self.user_info,
        sep = '\n'
        )


a = {
    'id': 1,
    'first_name': 0,
    'last_name': 1,
    # 'domain': 'domain'
}
# c = User(a,1)
# c.print_info()

