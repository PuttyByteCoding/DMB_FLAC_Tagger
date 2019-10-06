import sqlite3

class SongModel:
    def __init__(self, name, studio_album, live_debut):
        self.name = name
        self.studio_album = studio_album
        self.live_debut = live_debut

    def json(self):
        return {
            'name': self.name,
            'studio_album': self.studio_album,
            'live_debut': self.live_debut
        }


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM songs WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.commit()
        connection.close()

        if row:
            return cls(*row) # *row is the same as row[0], row[1], row[2]

    def insert(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO songs VALUES (?, ?, ?)"
        cursor.execute(query, (self.name, self.studio_album, self.live_debut))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE SONGS SET studio_album=? AND live_debut=? WHERE name=?"
        cursor.execute(query, (self.studio_album, self.live_debut, self.name))
        connection.commit()
        connection.close()