import requests
import tempfile
import re
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

ELEVENLABS_API_KEY = "sk_372a64047cfec111ed7f9cc95ee50b4e35d67f3654594981"
VOICE_ID = "XcWoPxj7pwnIgM3dQnWv"  # Deepa (Hindi female voice)

def clean_text(text):
    # Remove text in any brackets: [], (), 【】, etc.
    text = re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}|【.*?】|（.*?）", "", text)
    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()

@app.route('/tts', methods=['POST'])
def eleven_tts():
    try:
        data = request.get_json()
        raw_text = data.get("text", "")
        cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            return jsonify({"error": "Text is empty after cleaning"}), 400

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": cleaned_text,
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

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(response.content)
            audio_path = f.name

        return send_file(audio_path, mimetype="audio/mpeg", as_attachment=True, download_name="speech.mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
