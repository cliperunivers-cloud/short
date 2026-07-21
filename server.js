const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const COLAB_URL = process.env.COLAB_URL; // nanti kita isi

app.post('/generate', async (req, res) => {
    const { youtube_url } = req.body;
    try {
        const response = await axios.post(COLAB_URL, { url: youtube_url });
        res.json({ status: "success", videos: response.data.urls });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.get('/', (req,res) => res.send("Backend YT to Shorts jalan"))

app.listen(10000, () => console.log("Server jalan di port 10000"));
