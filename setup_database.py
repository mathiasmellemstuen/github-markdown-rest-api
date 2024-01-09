import sqlite3

database = sqlite3.connect("database.db")
database.execute("CREATE TABLE visitors(address, time)")