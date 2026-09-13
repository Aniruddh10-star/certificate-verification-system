import sqlite3

connection = sqlite3.connect("certificates.db")
cursor = connection.cursor()

cursor.execute(
    "SELECT certificate_id, certificate_hash FROM certificates"
)

records = cursor.fetchall()

for record in records:
    print("Certificate ID:", record[0])
    print("Hash:", record[1])
    print("----------------------")

connection.close()