import requests
import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self): # Handle CORS Preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            colab_url = os.environ.get('COLAB_URL')
            if not colab_url:
                self.send_error(500, "COLAB_URL belum diset di Vercel")
                return

            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)

            # HEADER PENTING BIAR LEWAT HALAMAN NGROK
            headers = {
                "ngrok-skip-browser-warning": "true",
                "Content-Type": "application/json"
            }

            r = requests.post(
                f"{colab_url}/api/process", 
                data=post_body, 
                headers=headers, 
                timeout=600 # 10 menit, karena render video lama
            )

            self.send_response(r.status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Kasih izin ke Flutter
            self.end_headers()
            self.wfile.write(r.content)

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
