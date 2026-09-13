import sqlite3

connection = sqlite3.connect("certificates.db")
cursor = connection.cursor()

cursor.execute("SELECT certificate_id, student_name, degree, year FROM certificates")

records = cursor.fetchall()

print("\n--- ALL CERTIFICATES ---")

for record in records:
    print("Certificate ID:", record[0])
    print("Student Name:", record[1])
    print("Degree:", record[2])
    print("Year:", record[3])
    print("----------------------")

connection.close()