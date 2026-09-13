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

with open("certificate_record.txt", "r") as file:
    saved_data = file.read()

if new_hash in saved_data:
    print("\n✅ CERTIFICATE IS VALID")
    print("Hash matches the stored record.")
else:
    print("\n❌ CERTIFICATE IS INVALID")
    print("Certificate data has been changed or is not registered.")