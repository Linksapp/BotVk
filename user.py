import json
#
class User:
    """Default User Class"""
    def __init__(self, user_info: dict, registration: bool = False) -> None:
        # Пользовательские данные
        if user_info == {}: self.create = False
        else:
            self.user_id = user_info['id']
            self.user_name = [user_info['first_name'], user_info['last_name']]
            # self.user_domain = user_info['domain']

            self.registratiom = registration
            self.create = True

        self.return_error(self.create)
        self.save_info()
    
    def get_info(self):
        pass

    def save_info(self):
        with open('dumb_db.txt', 'w', encoding='UTF-8') as f:
            f.write(f'{self.user_id} - {self.user_name}')
            return True
    
    def return_error(self, create: bool): 
        if create == False: raise BaseException('Error! Dont get user_info like full dict')
        else: pass

    def check_create(self) -> bool:
        """Дописать функцию"""
        with open('dumb_db.txt', 'r', encoding='UTF-8') as f:
            if self.user_id in f:
                return True
            else:
                self.save_info() # передовать все необходимые аргументы для сохранения
                return True

    def print_info(self):
        print(self.user_id,
        *self.user_name,
        # self.user_domain,
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