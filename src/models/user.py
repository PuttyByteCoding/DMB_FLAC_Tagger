import sqlite3

class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id #note: id is a python keyword, so I'm using _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row) # *row returns a tuple just like (row[0], row[1], row[2]) would.
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.dn")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)  # *row returns a tuple just like (row[0], row[1], row[2]) would.
        else:
            user = None

        connection.close()
        return user