export default async function handler(req, res) {
  // Cuma boleh method POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { url } = req.body;

    if (!url) {
      return res.status(400).json({ error: 'URL YouTube wajib diisi' });
    }

    // AMBIL LINK COLAB DARI ENVIRONMENT VARIABLE
    const COLAB_URL = process.env.COLAB_URL;

    if (!COLAB_URL) {
      return res.status(500).json({ error: 'COLAB_URL belum diset di Vercel' });
    }

    console.log("Menerima URL:", url);
    console.log("Meneruskan ke Colab:", COLAB_URL);

    // TERUSIN REQUEST KE COLAB
    const colabResponse = await fetch(`${COLAB_URL}/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url }),
      // Colab bisa lama, kasih timeout 10 menit
    });

    const data = await colabResponse.json();

    // KIRIM BALIKAN DARI COLAB KE FLUTTER
    return res.status(200).json(data);

  } catch (error) {
    console.error("Error di Vercel:", error);
    return res.status(500).json({ error: error.message });
  }
}
