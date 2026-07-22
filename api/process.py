import requests
import os
import json
import threading # TAMBAH INI
from http.server import BaseHTTPRequestHandler

def kirim_ke_colab(colab_url, body):
    headers = {"ngrok-skip-browser-warning": "true", "Content-Type": "application/json"}
    try:
        requests.post(f"{colab_url}/api/process", data=body, headers=headers, timeout=600)
    except: pass # Biarin jalan di belakang

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        colab_url = os.environ.get('COLAB_URL')
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len)

        # JALANKAN DI THREAD BIAR GA NUNGGU
        thread = threading.Thread(target=kirim_ke_colab, args=(colab_url, post_body))
        thread.start()

        # LANGSUNG BALAS KE FLUTTER
        self.send_response(202) # 202 = Accepted
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'diproses', 'message': 'Sedang membuat shorts di Colab. Cek Colab ya'}).encode())
