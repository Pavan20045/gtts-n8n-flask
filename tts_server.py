import requests
import tempfile
from flask import Flask, request, send_file, jsonify
import re

app = Flask(__name__)

ELEVENLABS_API_KEY = "sk_372a64047cfec111ed7f9cc95ee50b4e35d67f3654594981"  # Replace with your API Key
VOICE_ID = "XcWoPxj7pwnIgM3dQnWv"  # Deepa (Hindi female voice)

def clean_text(text):
    return re.sub(r"\[.*?\]", "", text)

@app.route('/tts', methods=['POST'])
def eleven_tts():
    try:
        data = request.get_json()
        text = clean_text(data.get("text", ""))
        if not text:
            return jsonify({"error": "Missing 'text' parameter"}), 400

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.6,
                "use_speaker_boost": True
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": response.json()}), 400

        # Save MP3 from binary stream
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(response.content)
            audio_path = f.name

        return send_file(audio_path, mimetype="audio/mpeg", as_attachment=True, download_name="speech.mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
