import json

class User:
    """Default User Class"""
    def __init__(self, user_info: dict, registration: bool = False) -> None:
        # Пользовательские данные
        if user_info == {} or len(user_info) < 4:
            self.create = False
            self.return_error()
        else:
            self.user_id = user_info['id']
            self.user_name = [user_info['first_name'], user_info['last_name']]
            self.user_domain = user_info['domain']

            self.registratiom = registration
            self.create = True
    
    def get_info(self):
        pass

    def save_info(self):
        pass

    def return_error(self): raise 'Error! Dont get user_info like full dict'

    def check_create(self):
        if self.create: return True
        else: return False

    def print_info(self):
        print(self.user_id,
        *self.user_name,
        self.user_domain,
        sep = '\n'
        )


a = {
    'id': 1,
    'first_name': 0,
    'last_name': 1,
    'domain': 'domain'
}