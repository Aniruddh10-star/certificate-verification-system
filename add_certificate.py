import sqlite3
import hashlib

certificate_id = input("Enter certificate ID: ")
student_name = input("Enter student name: ")
degree = input("Enter degree: ")
year = input("Enter graduation year: ")

certificate_data = certificate_id + student_name + degree + year

certificate_hash = hashlib.sha256(
    certificate_data.encode()
).hexdigest()

connection = sqlite3.connect("certificates.db")
cursor = connection.cursor()

cursor.execute(
    "INSERT INTO certificates (certificate_id, student_name, degree, year, certificate_hash) VALUES (?, ?, ?, ?, ?)",
    (certificate_id, student_name, degree, year, certificate_hash)
)

connection.commit()
connection.close()

print("\nCertificate added successfully!")
print("Certificate Hash:", certificate_hash)