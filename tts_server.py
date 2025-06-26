import os
import re
import requests
import tempfile
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

# Set your ElevenLabs API key here
ELEVENLABS_API_KEY = "sk_983d6d267c0aac14ce298b28e118612d3be3c026c885939d"
VOICE_ID = "XcWoPxj7pwnIgM3dQnWv"  # Deepa (Hindi female voice)

# Function to clean bracketed and unnecessary parts from the text
def clean_text(text):
    text = re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}|【.*?】|（.*?）", "", text)  # remove all bracketed content
    text = re.sub(r"\s+", " ", text)  # normalize multiple spaces
    return text.strip()

# TTS endpoint
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

# Required for deployment on Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
