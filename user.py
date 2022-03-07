import json

class User:
    """Default User Class"""
    def __init__(self, user_info: dict, registration: bool = False) -> None:
        # Пользовательские данные
        self.user_id = user_info['id']
        self.user_name = [user_info['first_name'], user_info['last_name']]
        # self.user_domain = user_info['domain']

        self.registration = registration
    
    def get_info(self):
        pass

    def save_info(self):
        with open('dumb_db.txt', 'w') as f:
            f.write(f'{self.user_id} - {self.user_name}')
            return True

    def check_create(self):
        with open('dumb_db.txt') as f:
            if self.user_id in f:
                return True
            else:
                User.save_info(self)
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
c = User(a,1)
c.print_info()