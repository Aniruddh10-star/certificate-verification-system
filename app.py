from flask import Flask, request, session, redirect, url_for
import sqlite3
import hashlib
import os
import psycopg2
from blockchain import Blockchain
import qrcode

DATABASE_URL = os.environ.get("DATABASE_URL")
def get_connection():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect("certificates.db")

app = Flask(__name__)
app.secret_key = "certificate_secret_key_2026"
os.makedirs("static", exist_ok=True)

if DATABASE_URL:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id BIGSERIAL PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        certificate_id TEXT UNIQUE,
        student_name TEXT,
        degree TEXT,
        year TEXT,
        certificate_hash TEXT
    )
    """)

    connection.commit()
    connection.close()

else:
    connection = get_connection()
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
    if not session.get("admin_logged_in"):
        return redirect("/admin")
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
<br><br>

<a href="/certificates">
    📋 View Registered Certificates
</a>
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

# ADMIN LOGIN

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect("/add")

        return """
        <h2>Invalid username or password</h2>
        <a href="/admin">Try Again</a>
        """

    return """
<!DOCTYPE html>
<html>

<head>
    <title>Admin Login</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .login-box {
            background: white;
            width: 360px;
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            text-align: center;
        }

        h1 {
            margin-bottom: 25px;
        }

        label {
            display: block;
            text-align: left;
            margin-top: 15px;
            font-weight: bold;
        }

        input {
            width: 100%;
            padding: 12px;
            margin-top: 7px;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 12px;
            margin-top: 25px;
            background: #1f4e79;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #163a5c;
        }

        .security {
            margin-top: 20px;
            font-size: 13px;
            color: #666;
        }
    </style>
</head>

<body>

    <div class="login-box">

        <h1>🔐 University Admin Login</h1>

        <form method="POST">

            <label>Username</label>
            <input type="text"
                   name="username"
                   placeholder="Enter admin username"
                   required>

            <label>Password</label>
            <input type="password"
                   name="password"
                   placeholder="Enter admin password"
                   required>

            <button type="submit">
                Login
            </button>

        </form>

        <div class="security">
            🔒 Authorized administrators only
        </div>

    </div>

</body>

</html>
"""
# ADMIN LOGOUT

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect("/admin")
# REGISTERED CERTIFICATES

@app.route("/certificates")
def registered_certificates():

    if not session.get("admin_logged_in"):
        return redirect("/admin")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT certificate_id, student_name, degree, year
        FROM certificates
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    html = """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Registered Certificates</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                padding: 30px;
            }

            .container {
                max-width: 1000px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.12);
            }

            h1 {
                text-align: center;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 25px;
            }

            th, td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }

            th {
                background: #1f4e79;
                color: white;
            }

            .delete {
                color: white;
                background: #c62828;
                padding: 7px 12px;
                text-decoration: none;
                border-radius: 5px;
            }

            .back {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>📋 Registered Certificates</h1>
    """

    for record in records:

        html += f"""
            <p>
                <b>Certificate ID:</b> {record[0]}<br>
                <b>Student:</b> {record[1]}<br>
                <b>Degree:</b> {record[2]}<br>
                <b>Year:</b> {record[3]}<br><br>

                <a class="delete"
                   href="/delete/{record[0]}"
                   onclick="return confirm('Delete this certificate?');">
                   🗑️ Delete
                </a>
            </p>

            <hr>
        """

    html += """
            <a class="back" href="/add">
                ← Back to Registration
            </a>
<br><br>

<a href="/logout">
    🚪 Admin Logout
</a>
        </div>

    </body>

    </html>
    """

    return html
# DELETE CERTIFICATE

@app.route("/delete/<certificate_id>")
def delete_certificate(certificate_id):

    if not session.get("admin_logged_in"):
        return redirect("/certificates")

    connection = get_connection()
    cursor = connection.cursor()

    # Delete certificate from database
    cursor.execute(
        "DELETE FROM certificates WHERE certificate_id = %s",
        (certificate_id,)
    )

    connection.commit()

    # Get all remaining certificates
    cursor.execute(
        "SELECT certificate_id, certificate_hash FROM certificates"
    )

    records = cursor.fetchall()
    connection.close()

    # Rebuild blockchain using remaining certificates
    blockchain = Blockchain()
    blockchain.chain = []

    for record in records:
        blockchain.add_block(
            record[0] + " | " + record[1]
        )

    blockchain.save_to_file()

    # Delete old QR code if it exists
    qr_file = "static/qr_" + certificate_id + ".png"

    if os.path.exists(qr_file):
        os.remove(qr_file)

    return redirect("/certificates")

# SAVE CERTIFICATE
# SAVE CERTIFICATE
@app.route("/add", methods=["POST"])
def add_certificate():
    if not session.get("admin_logged_in"):
        return redirect("/admin")

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

    connection = get_connection()
    cursor = connection.cursor()

    try:
        placeholder = "%s" if DATABASE_URL else "?"

        cursor.execute(
            f"""
            INSERT INTO certificates
            (certificate_id, student_name, degree, year, certificate_hash)
            VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
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

    except (sqlite3.IntegrityError, psycopg2.IntegrityError):
    connection.close()

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Certificate Already Exists</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #ffebee, #f5f7fa);
                margin: 0;
                padding: 0;
            }

            .header {
                background-color: #c62828;
                color: white;
                padding: 25px;
                text-align: center;
            }

            .container {
                width: 500px;
                max-width: 90%;
                margin: 70px auto;
                background: white;
                padding: 40px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            }

            .icon {
                font-size: 60px;
                margin-bottom: 15px;
            }

            h1 {
                color: #c62828;
                margin-bottom: 15px;
            }

            .message {
                color: #555;
                font-size: 16px;
                line-height: 1.6;
            }

            .warning {
                margin-top: 25px;
                padding: 15px;
                background: #ffebee;
                color: #c62828;
                border-radius: 8px;
                font-weight: bold;
            }

            .button {
                display: inline-block;
                margin-top: 30px;
                padding: 13px 25px;
                background: #1565c0;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
            }

            .button:hover {
                background: #0d47a1;
            }

            .home {
                display: block;
                margin-top: 20px;
                color: #1565c0;
                text-decoration: none;
            }

        </style>

    </head>

    <body>

        <div class="header">
            <h2>🎓 Certificate Verification System</h2>
        </div>

        <div class="container">

            <div class="icon">
                ⚠️
            </div>

            <h1>Certificate ID Already Exists</h1>

            <p class="message">
                This Certificate ID is already registered
                in the system.
            </p>

            <div class="warning">
                🔐 Each Certificate ID can only be registered once.
            </div>

            <a class="button" href="/add">
                🔄 Try Another Certificate
            </a>

            <a class="home" href="/">
                🏠 Back to Home
            </a>

        </div>

    </body>

    </html>
    """

    connection.close()

    # Add certificate to blockchain
    blockchain = Blockchain()

    blockchain.add_block(
        certificate_id + " | " + certificate_hash
    )

    blockchain.save_to_file()

    message = "✅ Certificate registered successfully!"

    qr_data = request.url_root + "verify"

    qr = qrcode.make(qr_data)

    qr_filename = "qr_" + certificate_id + ".png"

    qr.save(
        os.path.join(
            "static",
            qr_filename
        )
    )

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>Certificate Registered</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 30px 15px;
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                color: #222;
            }}

            .container {{
                max-width: 850px;
                margin: auto;
            }}

            .header {{
                background: #1565c0;
                color: white;
                padding: 25px;
                border-radius: 15px 15px 0 0;
                text-align: center;
            }}

            .header h1 {{
                margin: 0;
                font-size: 30px;
            }}

            .header p {{
                margin: 8px 0 0;
                opacity: 0.9;
            }}

            .card {{
                background: white;
                padding: 35px;
                border-radius: 0 0 15px 15px;
                box-shadow: 0 5px 25px rgba(0,0,0,0.12);
            }}

            .success {{
                text-align: center;
                margin-bottom: 30px;
            }}

            .success-icon {{
                font-size: 55px;
            }}

            .success h2 {{
                color: #2e7d32;
                margin: 10px 0;
            }}

            .success p {{
                color: #666;
            }}

            .details {{
                background: #f7f9fc;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 25px;
            }}

            .row {{
                display: flex;
                justify-content: space-between;
                padding: 12px 0;
                border-bottom: 1px solid #ddd;
                gap: 20px;
            }}

            .row:last-child {{
                border-bottom: none;
            }}

            .label {{
                font-weight: bold;
                color: #555;
            }}

            .value {{
                text-align: right;
                font-weight: 500;
            }}

            .hash-box {{
                background: #263238;
                color: #fff;
                padding: 15px;
                border-radius: 8px;
                word-break: break-all;
                font-family: monospace;
                font-size: 13px;
                margin-top: 8px;
            }}

            .qr-section {{
                text-align: center;
                margin: 30px 0;
                padding: 25px;
                background: #fafafa;
                border-radius: 12px;
                border: 1px solid #eee;
            }}

            .qr-section h3 {{
                margin-top: 0;
                color: #1565c0;
            }}

            .qr-section img {{
                width: 190px;
                height: 190px;
                margin: 15px;
            }}

            .qr-section p {{
                color: #666;
            }}

            .buttons {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
                margin-top: 30px;
            }}

            .button {{
                display: inline-block;
                padding: 13px 22px;
                border-radius: 8px;
                text-decoration: none;
                color: white;
                font-weight: bold;
                border: none;
                cursor: pointer;
                font-size: 15px;
            }}

            .print {{
                background: #1565c0;
            }}

            .verify {{
                background: #2e7d32;
            }}

            .home {{
                background: #546e7a;
            }}

            .button:hover {{
                opacity: 0.9;
            }}

            .footer {{
                text-align: center;
                color: #777;
                font-size: 13px;
                margin-top: 25px;
            }}

            @media (max-width: 600px) {{

                body {{
                    padding: 15px 8px;
                }}

                .card {{
                    padding: 20px 15px;
                }}

                .header h1 {{
                    font-size: 24px;
                }}

                .row {{
                    flex-direction: column;
                    gap: 5px;
                }}

                .value {{
                    text-align: left;
                }}

                .buttons {{
                    flex-direction: column;
                }}

                .button {{
                    width: 100%;
                    text-align: center;
                }}

                .qr-section img {{
                    width: 160px;
                    height: 160px;
                }}
            }}

        </style>
    </head>

    <body>

        <div class="container">

            <div class="header">
                <h1>🎓 Certificate Verification System</h1>
                <p>Blockchain-Based Academic Certificate Authentication</p>
            </div>

            <div class="card">

                <div class="success">
                    <div class="success-icon">✅</div>

                    <h2>Certificate Registered Successfully!</h2>

                    <p>
                        The academic certificate has been securely registered
                        in the verification system.
                    </p>
                </div>

                <div class="details">

                    <div class="row">
                        <span class="label">Certificate ID</span>
                        <span class="value">{certificate_id}</span>
                    </div>

                    <div class="row">
                        <span class="label">Student Name</span>
                        <span class="value">{student_name}</span>
                    </div>

                    <div class="row">
                        <span class="label">Degree</span>
                        <span class="value">{degree}</span>
                    </div>

                    <div class="row">
                        <span class="label">Graduation Year</span>
                        <span class="value">{year}</span>
                    </div>

                </div>

                <h3>🔐 Certificate SHA-256 Hash</h3>

                <div class="hash-box">
                    {certificate_hash}
                </div>

                <div class="qr-section">

                    <h3>📱 Certificate Verification QR Code</h3>

                    <img src="/static/{qr_filename}">

                    <p>
                        Scan this QR code to verify the certificate
                        through the online verification system.
                    </p>

                </div>

                <div class="buttons">

                    <a class="button print"
                       href="/certificate/{certificate_id}">
                        🖨️ Print Certificate
                    </a>

                    <a class="button verify"
                       href="/verify">
                        🔍 Verify Certificate
                    </a>

                    <a class="button home"
                       href="/">
                        🏠 Home
                    </a>

                </div>

                <div class="footer">
                    Blockchain-Based Anti-Forgery Academic Certificate
                    Verification System
                </div>

            </div>

        </div>

    </body>

    </html>
    """


# VERIFY CERTIFICATE PAGE
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

    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if DATABASE_URL else "?"

    cursor.execute(
        f"""
        SELECT certificate_id,
               student_name,
               degree,
               year,
               certificate_hash
        FROM certificates
        WHERE certificate_id = {placeholder}
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

    # Correct database field positions
    saved_certificate_id = record[0]
    saved_student_name = record[1]
    saved_degree = record[2]
    saved_year = record[3]
    saved_hash = record[4]

    # Check blockchain
    blockchain = Blockchain()

    blockchain_found = False

    for block in blockchain.chain:

        if block.data == certificate_id + " | " + saved_hash:

            blockchain_found = True
            break

    # Verify all information
    information_matches = (
        certificate_id == saved_certificate_id
        and student_name == saved_student_name
        and degree == saved_degree
        and year == saved_year
    )

    if (
        new_hash == saved_hash
        and blockchain_found
        and information_matches
    ):

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
                        <b>Certificate ID:</b> {saved_certificate_id}
                    </p>

                    <p>
                        <b>Student Name:</b> {saved_student_name}
                    </p>

                    <p>
                        <b>Degree:</b> {saved_degree}
                    </p>

                    <p>
                        <b>Graduation Year:</b> {saved_year}
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

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_name, degree, year, certificate_hash
        FROM certificates
        WHERE certificate_id = %s
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

    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if DATABASE_URL else "?"

    cursor.execute(
        f"""
        SELECT student_name, degree, year, certificate_hash
        FROM certificates
        WHERE certificate_id = {placeholder}
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

    </body>

    </html>
    """

# START SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
