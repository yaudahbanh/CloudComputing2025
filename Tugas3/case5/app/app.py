import os
from flask import Flask, render_template_string

app = Flask(__name__)
COUNT_FILE = "/app/data/count.txt"

@app.route('/')
def hello():
    count = 0
    if not os.path.exists(os.path.dirname(COUNT_FILE)):
        os.makedirs(os.path.dirname(COUNT_FILE))
        
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            try:
                count = int(f.read())
            except ValueError:
                count = 0
    
    count += 1
    with open(COUNT_FILE, 'w') as f:
        f.write(str(count))
        
    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Flask Persistent Counter</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-primary" role="alert">
                    <h1>Hello from Docker!</h1>
                    <p class="lead">Anda telah mengunjungi halaman ini sebanyak <strong>{{ count }}</strong> kali.</p>
                    <p>Coba restart kontainer atau bahkan hapus dan buat ulang, kunjungan Anda akan tetap tersimpan karena menggunakan Docker Volume!</p>
                </div>
            </div>
        </body>
        </html>
        """, count=count
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)