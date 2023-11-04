#!/usr/bin/env python3

from flask import Flask, request, send_file, Response
import qrcode
import base64
import urllib.parse
import re
from io import BytesIO

app = Flask(__name__)

# Regular expression to validate URLs
url_pattern = re.compile(r'^(http|https)://[^\s/$.?#].[^\s]*$')

@app.route('/')
def index():
    return '''
    <html>
    <body>
        <h1>hello</h1>
    </body>
    </html>
    '''

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(error):
    return "4-oh-4", 404

@app.route('/generate_qr')
def generate_qr_code():
    encoded_url = request.args.get('pg', '')  # Get the base64-encoded URL from the query string
    url = urllib.parse.unquote(base64.b64decode(encoded_url).decode('utf-8'))  # Decode the base64 data to get the URL

    if not url_pattern.match(url):
        return "Invalid URL"
    if len(url) > 1024:
        return "URL length exceeds 1024 characters"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to binary data
    img_binary = BytesIO()
    qr_img.save(img_binary)
    img_binary.seek(0)

    # Serve the QR code image as binary data with the appropriate MIME type
    return send_file(img_binary, mimetype="image/png")

if __name__ == '__main__':
    app.run()
