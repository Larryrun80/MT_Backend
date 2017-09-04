class User():
    """docstring for User"""

    def __init__(self, **params):
        '''Init user
           Load user data and return, using id or email/password
        '''
        self.id = 0
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id
