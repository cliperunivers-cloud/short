import requests
import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            colab_url = os.environ.get('COLAB_URL')
            if not colab_url:
                self._send(500, {'error': 'COLAB_URL belum diset di Vercel'})
                return

            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)

            headers = {
                "ngrok-skip-browser-warning": "true", # Biar lewatin halaman ngrok
                "Content-Type": "application/json"
            }

            # TIMEOUT 10 MENIT KARENA RENDER VIDEO LAMA
            r = requests.post(
                f"{colab_url}/api/process", 
                data=post_body, 
                headers=headers, 
                timeout=600
            )

            self._send(r.status_code, r.json())

        except requests.exceptions.Timeout:
            self._send(504, {'error': 'Colab kelamaan. Coba video yg lebih pendek'})
        except Exception as e:
            self._send(500, {'error': str(e)})
    
    def _send(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
