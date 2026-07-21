from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/process', methods=['POST', 'OPTIONS'])
def process():
    # Handle CORS buat Flutter
    if request.method == 'OPTIONS':
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }

    try:
        colab_url = os.environ.get('COLAB_URL')
        
        if not colab_url:
            return jsonify({'error': 'COLAB_URL belum diset di Vercel'}), 500

        data = request.get_json()
        youtube_url = data.get('url')
        jumlah_short = data.get('jumlah', 3)

        if not youtube_url:
            return jsonify({'error': 'URL YouTube kosong'}), 400

        r = requests.post(
            f"{colab_url}/process", 
            json={'url': youtube_url, 'jumlah': jumlah_short}, 
            timeout=600
        )

        return jsonify(r.json()), r.status_code, {
            'Access-Control-Allow-Origin': '*'
        }

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Timeout. Colab kelamaan proses'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# INI WAJIB BUAT VERCEL SERVERLESS
handler = app
