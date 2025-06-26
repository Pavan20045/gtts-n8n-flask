from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import tempfile
import os

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    try:
        data = request.get_json()
        text = data.get("text", "")
        lang = data.get("lang", "en")  # default to English if not provided

        if not text:
            return jsonify({"error": "Missing 'text' parameter"}), 400

        tts = gTTS(text=text, lang=lang)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)

        return send_file(temp_file.name, mimetype="audio/mpeg", as_attachment=True, download_name="speech.mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
