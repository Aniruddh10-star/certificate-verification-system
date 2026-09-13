import qrcode

data = "http://192.168.1.54:5000/verify/4ge23cs102"

qr = qrcode.make(data)

qr.save("certificate_qr.png")

print("Certificate QR code created successfully!")