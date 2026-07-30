import sqlite3

db = sqlite3.connect("storage/database/bot.db")

cursor = db.execute("PRAGMA table_info(users)")

for row in cursor.fetchall():
    print(row)

db.close()