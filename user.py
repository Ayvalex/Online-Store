class User:
    def __init__(self, username=None, password=None, confirm_password=None, first_name=None, last_name=None,
                 email=None):
        self.username = username
        self.password = password
        self.confirm_password = confirm_password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
