import sqlite3

conn = sqlite3.connect('database/password_managers.db')
c = conn.cursor()
c.execute("SELECT * FROM password_managers")
result = c.fetchall()
print(result)
conn.close()