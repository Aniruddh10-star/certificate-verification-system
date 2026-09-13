import sqlite3
import hashlib

print("--- CERTIFICATE VERIFICATION ---")

certificate_id = input("Enter certificate ID: ")
student_name = input("Enter student name: ")
degree = input("Enter degree: ")
year = input("Enter graduation year: ")

certificate_data = certificate_id + student_name + degree + year

new_hash = hashlib.sha256(
    certificate_data.encode()
).hexdigest()

connection = sqlite3.connect("certificates.db")
cursor = connection.cursor()

cursor.execute(
    "SELECT certificate_hash FROM certificates WHERE certificate_id = ?",
    (certificate_id,)
)

record = cursor.fetchone()

if record is None:
    print("\n❌ CERTIFICATE NOT FOUND")
else:
    saved_hash = record[0]

    if new_hash == saved_hash:
        print("\n✅ CERTIFICATE IS VALID")
        print("Hash matches the database record.")
    else:
        print("\n❌ CERTIFICATE IS INVALID")
        print("Certificate information has been changed.")

connection.close()