import sqlite3

DEFAULT_DATABASE = 'trth.db'
REQUEST_DATABASE = 'request.db'

def connect(database=DEFAULT_DATABASE):
    return sqlite3.connect(database)

def get_table_names(db):
    with db:
        c = db.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
        tables = [x[0] for x in c.fetchall()]
    return tables
