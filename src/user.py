class User:
    def __init__(self, _id, username, password):
        self.id = _id #note: id is a python keyword, so I'm using _id
        self.username = username
        self.password = password