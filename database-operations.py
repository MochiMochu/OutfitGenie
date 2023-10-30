import sqlite3

conn = sqlite3.connect("user_logins.db")
c = conn.cursor()
c.execute("""CREATE TABLE """)