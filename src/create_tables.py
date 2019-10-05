import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = f"CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()
connection.close()

#
# users = [
#     (1, 'putty', 'PuttyPass'),
#     (2, 'jack', 'JacksonPass'),
#     (3, 'katie', 'KatiePass'),
# ]
#
# insert_query = f"INSERT INTO users VALUES(?, ?, ?)"
# cursor.executemany(insert_query, users)
#
#
# select_query = "SELECT * FROM users"
# for row in cursor.execute(select_query):
#     print(row)
#
#
