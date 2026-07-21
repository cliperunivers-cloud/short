from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/process', methods=['POST', 'OPTIONS'])
def process():
    # Buat handle CORS dari Flutter
    if request.method == 'OPTIONS':
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }

    try:
        # Ambil URL Colab dari Environment Variables Vercel
        colab_url = os.environ.get('COLAB_URL')
        
        if not colab_url:
            return jsonify({'error': 'COLAB_URL belum diset di Vercel'}), 500

        # Ambil data dari Flutter
        data = request.get_json()
        youtube_url = data.get('url')
        jumlah_short = data.get('jumlah', 3)

        if not youtube_url:
            return jsonify({'error': 'URL YouTube kosong'}), 400

        # Kirim ke Colab/ngrok
        r = requests.post(
            f"{colab_url}/process", 
            json={
                'url': youtube_url,
                'jumlah': jumlah_short
            }, 
            timeout=600  # 10 menit, karena proses yt-dlp lama
        )

        # Balikin hasil dari Colab ke Flutter
        return jsonify(r.json()), r.status_code, {
            'Access-Control-Allow-Origin': '*'
        }

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Timeout. Colab kelamaan proses'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ini wajib buat Vercel Serverless
def handler(req, res):
    return app(req, res)
    const COLAB_URL = process.env.COLAB_URL;
    if (!COLAB_URL) {
      return res.status(500).json({ error: 'COLAB_URL belum diset di Vercel' });
    }

    // Pake http/https bawaan
    const response = await fetch(`${COLAB_URL}/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();
    return res.status(200).json(data);

  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
