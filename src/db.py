import sqlite3

DEFAULT_DATABASE = 'trth.db'

def connect(database=DEFAULT_DATABASE):
    return sqlite3.connect(database)
