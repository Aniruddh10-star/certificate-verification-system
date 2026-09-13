from flask import Flask, request
import sqlite3
import hashlib
import os
from blockchain import Blockchain
import qrcode

app = Flask(__name__)
os.makedirs("static", exist_ok=True)

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
connection.commit()
connection.close()

# HOME PAGE
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Certificate Verification System</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #e3f2fd, #f5f7fa);
                margin: 0;
                padding: 0;
            }

            .header {
                background-color: #1565c0;
                color: white;
                padding: 25px;
                text-align: center;
            }

            .container {
                width: 700px;
                max-width: 90%;
                margin: 50px auto;
                background: white;
                padding: 40px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            }

            h1 {
                margin-bottom: 10px;
            }

            .subtitle {
                color: #555;
                font-size: 18px;
                margin-bottom: 35px;
            }

            .button {
                display: inline-block;
                width: 250px;
                margin: 10px;
                padding: 15px;
                text-decoration: none;
                color: white;
                background-color: #1565c0;
                border-radius: 8px;
                font-size: 16px;
            }

            .button:hover {
                background-color: #0d47a1;
            }

            .info {
                margin-top: 35px;
                padding: 20px;
                background-color: #f5f5f5;
                border-radius: 10px;
            }

            .footer {
                text-align: center;
                color: #777;
                margin-top: 30px;
            }
        </style>

    </head>

    <body>

        <div class="header">
            <h1>🎓 Certificate Verification System</h1>
            <p>Blockchain-Based Anti-Forgery Platform</p>
        </div>

        <div class="container">

            <h2>Welcome</h2>

            <p class="subtitle">
                Securely register and verify academic certificates
                using cryptographic hashing and blockchain technology.
            </p>

            <a class="button" href="/add">
                🎓 Register Certificate
            </a>

            <a class="button" href="/verify">
                🔍 Verify Certificate
            </a>

            <div class="info">

                <h3>🔐 Security Features</h3>

                <p>✔ SHA-256 Certificate Hashing</p>
                <p>✔ Blockchain Record Verification</p>
                <p>✔ QR Code Verification</p>
                <p>✔ Forgery Detection</p>

            </div>

        </div>

        <div class="footer">
            <p>Academic Certificate Authentication System</p>
        </div>

    </body>

    </html>
    """


# REGISTER CERTIFICATE PAGE
@app.route("/add")
def add_certificate_page():
    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Register Certificate</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #e3f2fd, #f5f7fa);
                margin: 0;
                padding: 0;
            }

            .header {
                background-color: #1565c0;
                color: white;
                padding: 25px;
                text-align: center;
            }

            .container {
                width: 500px;
                max-width: 90%;
                margin: 45px auto;
                background: white;
                padding: 35px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            }

            h1 {
                text-align: center;
                color: #1565c0;
            }

            .description {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }

            label {
                display: block;
                margin-bottom: 7px;
                font-weight: bold;
            }

            input {
                width: 100%;
                box-sizing: border-box;
                padding: 12px;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 7px;
                font-size: 15px;
            }

            input:focus {
                border-color: #1565c0;
                outline: none;
            }

            button {
                width: 100%;
                padding: 14px;
                border: none;
                border-radius: 8px;
                background-color: #1565c0;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover {
                background-color: #0d47a1;
            }

            .back {
                display: block;
                text-align: center;
                margin-top: 25px;
                text-decoration: none;
                color: #1565c0;
            }

            .security {
                margin-top: 25px;
                padding: 15px;
                background-color: #f5f5f5;
                border-radius: 8px;
                text-align: center;
                color: #555;
            }

        </style>

    </head>

    <body>

        <div class="header">
            <h2>🎓 Certificate Verification System</h2>
        </div>

        <div class="container">

            <h1>🎓 Register Certificate</h1>

            <p class="description">
                Register an academic certificate securely
                in the verification system.
            </p>

            <form action="/add" method="post">

                <label>Certificate ID</label>

                <input type="text"
                       name="certificate_id"
                       placeholder="Enter Certificate ID"
                       required>

                <label>Student Name</label>

                <input type="text"
                       name="student_name"
                       placeholder="Enter Student Name"
                       required>

                <label>Degree</label>

                <input type="text"
                       name="degree"
                       placeholder="Enter Degree"
                       required>

                <label>Graduation Year</label>

                <input type="text"
                       name="year"
                       placeholder="Enter Graduation Year"
                       required>

                <button type="submit">
                    🔐 Register Certificate
                </button>

            </form>

            <div class="security">
                🔒 Certificate data is protected using
                SHA-256 hashing and blockchain verification.
            </div>

            <a class="back" href="/">
                🏠 Back to Home
            </a>

        </div>

    </body>

    </html>
    """


# SAVE CERTIFICATE
@app.route("/add", methods=["POST"])
def add_certificate():

    certificate_id = request.form["certificate_id"]
    student_name = request.form["student_name"]
    degree = request.form["degree"]
    year = request.form["year"]

    certificate_data = (
        certificate_id +
        student_name +
        degree +
        year
    )

    certificate_hash = hashlib.sha256(
        certificate_data.encode()
    ).hexdigest()

    connection = sqlite3.connect("certificates.db")
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO certificates
            (certificate_id, student_name, degree, year, certificate_hash)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                certificate_id,
                student_name,
                degree,
                year,
                certificate_hash
            )
        )

        connection.commit()

        # Add certificate to blockchain
        blockchain = Blockchain()

        blockchain.add_block(
            certificate_id + " | " + certificate_hash
        )

        blockchain.save_to_file()

        message = "✅ Certificate registered successfully!"
        blockchain.save_to_file()

        message = "✅ Certificate registered successfully!"

        # Generate QR code
        qr_data = request.host_url + "verify/" + certificate_id

        qr = qrcode.make(qr_data)

        qr_filename = "static/qr_" + certificate_id + ".png"

        qr.save(qr_filename)

    except sqlite3.IntegrityError:

        message = "❌ Certificate ID already exists!"
        qr_filename = ""
    connection.close()

    return f"""
<!DOCTYPE html>
<html>

<head>

    <title>Certificate Registered</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #e3f2fd, #f5f7fa);
            margin: 0;
            padding: 0;
        }}

        .header {{
            background-color: #1565c0;
            color: white;
            padding: 25px;
            text-align: center;
        }}

        .container {{
            width: 600px;
            max-width: 90%;
            margin: 45px auto;
            background: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}

        .success {{
            color: #2e7d32;
            font-size: 26px;
            font-weight: bold;
        }}

        .details {{
            margin-top: 25px;
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 10px;
            text-align: left;
        }}

        .qr {{
            margin-top: 25px;
        }}

        .qr img {{
            width: 220px;
            height: 220px;
        }}

        .instruction {{
            color: #555;
            margin-top: 15px;
        }}

        a {{
            display: block;
            margin-top: 25px;
            text-decoration: none;
            color: #1565c0;
        }}

    </style>

</head>

<body>

    <div class="header">
        <h2>🎓 Certificate Verification System</h2>
        <p>Blockchain-Based Anti-Forgery Platform</p>
    </div>

    <div class="container">

        <div class="success">
            {message}
        </div>

        <div class="details">

            <p>
                <b>Certificate ID:</b> {certificate_id}
            </p>

            <p>
                <b>Hash:</b> {certificate_hash}
            </p>

        </div>

        <div class="qr">

            <h2>📱 Certificate QR Code</h2>

            <img src="/static/{qr_filename.split('/')[-1]}">

            <p class="instruction">
                Scan this QR code to verify the certificate.
            </p>

        </div>

        <a href="/">
            🏠 Back to Home
        </a>
        <a href="/certificate/{certificate_id}">
       📜 View / Print Certificate
       </a>
        <a href="/verify">
            🔍 Verify Certificate
        </a>

    </div>

</body>

</html>
"""


# VERIFY CERTIFICATE PAGE
@app.route("/verify", methods=["GET", "POST"])
def verify():

    if request.method == "GET":

        return """
        <!DOCTYPE html>
        <html>

        <head>

            <title>Verify Certificate</title>

            <style>

                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #e3f2fd, #f5f7fa);
                    margin: 0;
                    padding: 0;
                }

                .header {
                    background-color: #1565c0;
                    color: white;
                    padding: 25px;
                    text-align: center;
                }

                .container {
                    width: 500px;
                    max-width: 90%;
                    margin: 45px auto;
                    background: white;
                    padding: 35px;
                    border-radius: 15px;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                }

                h1 {
                    text-align: center;
                    color: #1565c0;
                }

                .description {
                    text-align: center;
                    color: #666;
                    margin-bottom: 30px;
                }

                label {
                    display: block;
                    margin-bottom: 7px;
                    font-weight: bold;
                }

                input {
                    width: 100%;
                    box-sizing: border-box;
                    padding: 12px;
                    margin-bottom: 20px;
                    border: 1px solid #ccc;
                    border-radius: 7px;
                    font-size: 15px;
                }

                button {
                    width: 100%;
                    padding: 14px;
                    border: none;
                    border-radius: 8px;
                    background-color: #1565c0;
                    color: white;
                    font-size: 16px;
                    cursor: pointer;
                }

                .security {
                    margin-top: 25px;
                    padding: 15px;
                    background-color: #f5f5f5;
                    border-radius: 8px;
                    text-align: center;
                    color: #555;
                }

                .back {
                    display: block;
                    text-align: center;
                    margin-top: 25px;
                    text-decoration: none;
                    color: #1565c0;
                }

            </style>

        </head>

        <body>

            <div class="header">
                <h2>🎓 Certificate Verification System</h2>
            </div>

            <div class="container">

                <h1>🔍 Verify Certificate</h1>

                <p class="description">
                    Verify the authenticity of an academic certificate
                    using hashing and blockchain technology.
                </p>

                <form action="/verify" method="post">

                    <label>Certificate ID</label>

                    <input type="text"
                           name="certificate_id"
                           placeholder="Enter Certificate ID"
                           required>

                    <label>Student Name</label>

                    <input type="text"
                           name="student_name"
                           placeholder="Enter Student Name"
                           required>

                    <label>Degree</label>

                    <input type="text"
                           name="degree"
                           placeholder="Enter Degree"
                           required>

                    <label>Graduation Year</label>

                    <input type="text"
                           name="year"
                           placeholder="Enter Graduation Year"
                           required>

                    <button type="submit">
                        🔍 Verify Certificate
                    </button>

                </form>

                <div class="security">
                    🔐 Verification checks the certificate hash
                    and blockchain record.
                </div>

                <a class="back" href="/">
                    🏠 Back to Home
                </a>

            </div>

        </body>

        </html>
        """

    certificate_id = request.form["certificate_id"]
    student_name = request.form["student_name"]
    degree = request.form["degree"]
    year = request.form["year"]

    certificate_data = (
        certificate_id +
        student_name +
        degree +
        year
    )

    new_hash = hashlib.sha256(
        certificate_data.encode()
    ).hexdigest()

    connection = sqlite3.connect("certificates.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT certificate_hash
        FROM certificates
        WHERE certificate_id = ?
        """,
        (certificate_id,)
    )

    record = cursor.fetchone()

    connection.close()

    if record is None:

        return """
        <h1>❌ Certificate Not Found</h1>
        <a href="/verify">Try Again</a>
        """

    saved_hash = record[0]

    blockchain = Blockchain()

    blockchain_found = False

    for block in blockchain.chain:

        if block.data == certificate_id + " | " + saved_hash:
            blockchain_found = True
            break

    if new_hash == saved_hash and blockchain_found:

        return f"""
        <!DOCTYPE html>
        <html>

        <head>
            <title>Certificate Verified</title>

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    background: #f5f7fa;
                    margin: 0;
                    padding: 0;
                }}

                .container {{
                    width: 600px;
                    max-width: 90%;
                    margin: 60px auto;
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                }}

                .valid {{
                    text-align: center;
                    color: #2e7d32;
                    font-size: 28px;
                    font-weight: bold;
                }}

                .details {{
                    margin-top: 25px;
                    padding: 20px;
                    background: #f5f5f5;
                    border-radius: 10px;
                }}

                .check {{
                    margin-top: 10px;
                    padding: 12px;
                    background: #e8f5e9;
                    color: #2e7d32;
                    border-radius: 7px;
                    font-weight: bold;
                }}

                a {{
                    display: block;
                    text-align: center;
                    margin-top: 25px;
                    text-decoration: none;
                    color: #1565c0;
                }}

            </style>

        </head>

        <body>

            <div class="container">

                <div class="valid">
                    ✅ CERTIFICATE IS VALID
                </div>

                <div class="details">

                    <h2>🎓 Certificate Details</h2>

                    <p>
                        <b>Certificate ID:</b> {certificate_id}
                    </p>

                    <p>
                        <b>Student Name:</b> {student_name}
                    </p>

                    <p>
                        <b>Degree:</b> {degree}
                    </p>

                    <p>
                        <b>Graduation Year:</b> {year}
                    </p>

                </div>

                <div class="check">
                    ✅ SHA-256 Hash Verified
                </div>

                <div class="check">
                    ✅ Blockchain Record Verified
                </div>

                <div class="check">
                    ✅ Certificate Information Matches
                </div>

                <a href="/">
                    🏠 Back to Home
                </a>

            </div>

        </body>

        </html>
        """

    else:

        return """
        <!DOCTYPE html>
        <html>

        <head>

            <title>Certificate Invalid</title>

            <style>

                body {
                    font-family: Arial, sans-serif;
                    background: #f5f7fa;
                    margin: 0;
                    padding: 0;
                }

                .container {
                    width: 600px;
                    max-width: 90%;
                    margin: 80px auto;
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                }

                h1 {
                    color: #c62828;
                }

                .warning {
                    margin-top: 25px;
                    padding: 15px;
                    background: #ffebee;
                    color: #c62828;
                    border-radius: 8px;
                    font-weight: bold;
                }

                a {
                    display: block;
                    margin-top: 25px;
                    text-decoration: none;
                    color: #1565c0;
                }

            </style>

        </head>

        <body>

            <div class="container">

                <h1>❌ CERTIFICATE IS INVALID</h1>

                <p>
                    The certificate information does not match
                    the stored database or blockchain record.
                </p>

                <div class="warning">
                    ⚠️ Possible forged or modified certificate
                </div>

                <a href="/verify">
                    🔍 Try Verification Again
                </a>

                <a href="/">
                    🏠 Back to Home
                </a>

            </div>

        </body>

        </html>
        """
# QR CODE VERIFICATION
@app.route("/verify/<certificate_id>")
def verify_qr(certificate_id):

    connection = sqlite3.connect("certificates.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_name, degree, year, certificate_hash
        FROM certificates
        WHERE certificate_id = ?
        """,
        (certificate_id,)
    )

    record = cursor.fetchone()

    connection.close()

    # CERTIFICATE NOT FOUND
    if record is None:

        return """
        <!DOCTYPE html>
        <html>

        <head>
            <title>Certificate Not Found</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #e3f2fd, #f5f7fa);
                    margin: 0;
                    padding: 0;
                }

                .header {
                    background-color: #1565c0;
                    color: white;
                    padding: 25px;
                    text-align: center;
                }

                .container {
                    width: 600px;
                    max-width: 90%;
                    margin: 60px auto;
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                }

                h1 {
                    color: #c62828;
                }

                .warning {
                    margin-top: 25px;
                    padding: 15px;
                    background-color: #ffebee;
                    color: #c62828;
                    border-radius: 8px;
                    font-weight: bold;
                }

                a {
                    display: block;
                    margin-top: 25px;
                    text-decoration: none;
                    color: #1565c0;
                }
            </style>

        </head>

        <body>

            <div class="header">
                <h2>🎓 Certificate Verification System</h2>
            </div>

            <div class="container">

                <h1>❌ CERTIFICATE NOT FOUND</h1>

                <p>
                    This certificate ID does not exist
                    in the verification system.
                </p>

                <div class="warning">
                    ⚠️ Unable to verify this certificate
                </div>

                <a href="/">
                    🏠 Back to Home
                </a>

            </div>

        </body>

        </html>
        """

    student_name = record[0]
    degree = record[1]
    year = record[2]
    saved_hash = record[3]

    certificate_data = (
        certificate_id +
        student_name +
        degree +
        year
    )

    calculated_hash = hashlib.sha256(
        certificate_data.encode()
    ).hexdigest()

    blockchain = Blockchain()

    blockchain_found = False

    for block in blockchain.chain:

        if block.data == certificate_id + " | " + saved_hash:
            blockchain_found = True
            break

    # VALID CERTIFICATE
    if calculated_hash == saved_hash and blockchain_found:

        return f"""
        <!DOCTYPE html>
        <html>

        <head>
            <title>Certificate Verified</title>

            <style>

                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #e3f2fd, #f5f7fa);
                    margin: 0;
                    padding: 0;
                }}

                .header {{
                    background-color: #1565c0;
                    color: white;
                    padding: 25px;
                    text-align: center;
                }}

                .container {{
                    width: 600px;
                    max-width: 90%;
                    margin: 45px auto;
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                }}

                .valid {{
                    text-align: center;
                    color: #2e7d32;
                    font-size: 28px;
                    font-weight: bold;
                }}

                .verified-message {{
                    text-align: center;
                    color: #555;
                    margin-top: 10px;
                    margin-bottom: 30px;
                }}

                .details {{
                    padding: 20px;
                    background-color: #f5f5f5;
                    border-radius: 10px;
                }}

                .details h2 {{
                    color: #1565c0;
                }}

                .check {{
                    margin-top: 12px;
                    padding: 13px;
                    background-color: #e8f5e9;
                    color: #2e7d32;
                    border-radius: 7px;
                    font-weight: bold;
                }}

                .authentic {{
                    margin-top: 25px;
                    padding: 18px;
                    background-color: #e3f2fd;
                    border-radius: 10px;
                    text-align: center;
                    color: #1565c0;
                    font-weight: bold;
                }}

                a {{
                    display: block;
                    text-align: center;
                    margin-top: 25px;
                    text-decoration: none;
                    color: #1565c0;
                }}

            </style>

        </head>

        <body>

            <div class="header">
                <h2>🎓 Certificate Verification System</h2>
                <p>Blockchain-Based Anti-Forgery Platform</p>
            </div>

            <div class="container">

                <div class="valid">
                    ✅ CERTIFICATE IS VALID
                </div>

                <p class="verified-message">
                    This certificate has been successfully verified.
                </p>

                <div class="details">

                    <h2>🎓 Certificate Details</h2>

                    <p>
                        <b>Certificate ID:</b> {certificate_id}
                    </p>

                    <p>
                        <b>Student Name:</b> {student_name}
                    </p>

                    <p>
                        <b>Degree:</b> {degree}
                    </p>

                    <p>
                        <b>Graduation Year:</b> {year}
                    </p>

                </div>

                <div class="check">
                    ✅ SHA-256 Hash Verified
                </div>

                <div class="check">
                    ✅ Blockchain Record Verified
                </div>

                <div class="check">
                    ✅ Certificate Information Verified
                </div>

                <div class="authentic">
                    🔐 This academic certificate is authentic.
                </div>

                <a href="/">
                    🏠 Back to Home
                </a>

            </div>

        </body>

        </html>
        """

    # INVALID CERTIFICATE
    else:

        return """
        <!DOCTYPE html>
        <html>

        <head>
            <title>Invalid Certificate</title>

            <style>

                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #e3f2fd, #f5f7fa);
                    margin: 0;
                    padding: 0;
                }

                .header {
                    background-color: #1565c0;
                    color: white;
                    padding: 25px;
                    text-align: center;
                }

                .container {
                    width: 600px;
                    max-width: 90%;
                    margin: 60px auto;
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                }

                h1 {
                    color: #c62828;
                }

                .warning {
                    margin-top: 25px;
                    padding: 18px;
                    background-color: #ffebee;
                    color: #c62828;
                    border-radius: 8px;
                    font-weight: bold;
                }

                a {
                    display: block;
                    margin-top: 25px;
                    text-decoration: none;
                    color: #1565c0;
                }

            </style>

        </head>

        <body>

            <div class="header">
                <h2>🎓 Certificate Verification System</h2>
            </div>

            <div class="container">

                <h1>❌ CERTIFICATE IS INVALID</h1>

                <p>
                    The certificate failed security verification.
                </p>

                <div class="warning">
                    ⚠️ The certificate may have been modified or forged.
                </div>

                <a href="/">
                    🏠 Back to Home
                </a>

            </div>

        </body>

        </html>
        """
# PRINTABLE CERTIFICATE
@app.route("/certificate/<certificate_id>")
def certificate(certificate_id):

    connection = sqlite3.connect("certificates.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_name, degree, year, certificate_hash
        FROM certificates
        WHERE certificate_id = ?
        """,
        (certificate_id,)
    )

    record = cursor.fetchone()

    connection.close()

    if record is None:
        return """
        <h1>❌ Certificate Not Found</h1>
        <a href="/">🏠 Back to Home</a>
        """

    student_name = record[0]
    degree = record[1]
    year = record[2]

    qr_filename = "qr_" + certificate_id + ".png"

    return f"""
    <!DOCTYPE html>
    <html>

    <head>

        <title>Academic Certificate</title>

        <style>
        button {{
            padding: 12px 25px;
            background-color: #1565c0;
            color: white;
            border: none;
            border-radius: 7px;
            font-size: 16px;
            cursor: pointer;
        }}

        button:hover {{
            background-color: #0d47a1;
        }}

        @media print {{
            button {{
                display: none;
            }}

            body {{
                background: white;
                padding: 0;
            }}

            .certificate {{
                box-shadow: none;
            }}
        }}

            body {{
                font-family: Georgia, serif;
                background-color: #f2f2f2;
                margin: 0;
                padding: 30px;
            }}

            .certificate {{
                width: 800px;
                max-width: 90%;
                margin: auto;
                padding: 50px;
                background-color: white;
                border: 8px solid #1565c0;
                text-align: center;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            }}

            h1 {{
                color: #1565c0;
                font-size: 36px;
            }}

            h2 {{
                margin-top: 30px;
            }}

            .student {{
                font-size: 30px;
                font-weight: bold;
                margin: 25px;
            }}

            .degree {{
                font-size: 22px;
                margin: 20px;
            }}

            .details {{
                margin-top: 30px;
                font-family: Arial, sans-serif;
            }}

            .qr {{
                margin-top: 30px;
            }}

            .qr img {{
                width: 160px;
                height: 160px;
            }}

            .verification {{
                font-family: Arial, sans-serif;
                color: #555;
                margin-top: 10px;
            }}

        </style>

    </head>

    <body>

        <div class="certificate">

            <h1>🎓 ACADEMIC CERTIFICATE</h1>

            <p>This is to certify that</p>

            <div class="student">
                {student_name}
            </div>

            <p>has successfully completed the degree</p>

            <div class="degree">
                <b>{degree}</b>
            </div>

            <p>Graduation Year: <b>{year}</b></p>

            <div class="details">

                <p>
                    <b>Certificate ID:</b> {certificate_id}
                </p>

            </div>

            <div class="qr">

                <h3>📱 Scan to Verify Certificate</h3>

                <img src="/static/{qr_filename}">

                <p class="verification">
                    This QR code connects to the
                    certificate verification system.
                </p>

            </div>
<br><br>

<button onclick="window.print()">
    🖨️ Print Certificate
</button>                 
        </div>

    </html>
    """

# START SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
