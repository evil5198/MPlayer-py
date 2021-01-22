import sqlite3

conn = sqlite3.connect('seconds.db')

cursor = conn.execute("SELECT second from Seconds")

for row in cursor:
    print(row[0])

conn.execute("UPDATE Seconds set second = 0")
conn.commit()

cursor = conn.execute("SELECT second from Seconds")

for row in cursor:
    print(row[0])