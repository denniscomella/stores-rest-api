import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)" # INTEGER creates auto-incrementing number columns (cannot use "int" data type although it usually doesn't matter
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

# cursor.execute("INSERT INTO items VALUES ('test', 10.99)") # test data ONLY

connection.commit()

connection.close()