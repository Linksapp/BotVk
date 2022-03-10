import database
#

"""Переделать класс, создать модуль для записи информации в бд"""

class User:
    """Default User Class"""
    def __init__(self, user_info: dict, registration: bool = False) -> None:
        # Пользовательские данные
        if user_info == {}: self.create = False
        else:
            self.user_info = user_info
            self.registratiom = registration
            self.create = True

        database.save_info(self.user_info)
        self.return_error()  # закоментил, надо куда-то это сунуть или ещё раз объясни почему именно здесь стоит.
         
    
    def return_error(self): 
        if self.create == False: raise BaseException('Error! Dont get user_info like full dict')

    def print_info(self):
        print(self.user_info,
        sep = '\n')

