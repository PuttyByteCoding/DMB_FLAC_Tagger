import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_users_table)

create_songs_table = "CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name text, studio_album text, live_debut text)"
cursor.execute(create_songs_table)

# Populate with song samples
# insert_sample_songs_query = "INSERT INTO songs VALUES(?, ?, ?, ?)"
# sample_songs = [
#     (1, "Too Much", "Crash", "1994-10-04"),
#     (2, "Two Step", "Crash", "1992-03-16"),
#     (3, "Don't Drink the Water", "Before these crowded streets", "1998-04-16"),
#     (4, "Warehouse", "Under the Table And Dreaming", "1991-02-19"),
# ]
# cursor.executemany(insert_sample_songs_query, sample_songs)

connection.commit()
connection.close()
