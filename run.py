import sqlite3

conn = sqlite3.connect("test.db")
c = conn.cursor()

try:
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username VARCHAR(32) UNIQUE NOT NULL,
        password_hash VARCHAR(200))''')
except sqlite3.OperationalError as e:
    print('sqlite error:', e.args[0])  # table companies already exists

conn.commit()

try:
    c.execute('''CREATE TABLE moods (
        id INTEGER PRIMARY KEY,
        uid INTEGER,
        mood VARCHAR(32) NOT NULL,
        created DATETIME default current_timestamp,
        streak INTEGER,
        FOREIGN KEY (uid) REFERENCES users (id))''')
except sqlite3.OperationalError as e:
    print('sqlite error:', e.args[0])  # table companies already exists

conn.commit()

conn.close()

print('done')
