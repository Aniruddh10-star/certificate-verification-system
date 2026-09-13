import sqlite3

connection = sqlite3.connect("certificates.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    certificate_id TEXT UNIQUE,
    student_name TEXT,
    degree TEXT,
    year TEXT,
    certificate_hash TEXT
)
""")

connection.commit()
connection.close()

print("Database created successfully!")