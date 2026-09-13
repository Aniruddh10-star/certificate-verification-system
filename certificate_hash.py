import hashlib

certificate_id = input("Enter certificate ID: ")
student_name = input("Enter student name: ")
degree = input("Enter degree: ")
year = input("Enter graduation year: ")

certificate_data = certificate_id + student_name + degree + year

certificate_hash = hashlib.sha256(
    certificate_data.encode()
).hexdigest()

print("\n--- CERTIFICATE RECORD ---")
print("Certificate ID:", certificate_id)
print("Student Name:", student_name)
print("Degree:", degree)
print("Year:", year)
print("SHA-256 Hash:", certificate_hash)

with open("certificate_record.txt", "w") as file:
    file.write("Certificate ID: " + certificate_id + "\n")
    file.write("Student Name: " + student_name + "\n")
    file.write("Degree: " + degree + "\n")
    file.write("Year: " + year + "\n")
    file.write("SHA-256 Hash: " + certificate_hash + "\n")

print("\nCertificate record saved successfully!")