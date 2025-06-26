from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    try:
        data = request.get_json()
        text = data.get('text', '')
        lang = data.get('lang', 'en')

        if not text:
            return jsonify({'error': 'Text is required'}), 400

        filename = f"{uuid.uuid4().hex}.mp3"
        tts = gTTS(text, lang=lang)
        tts.save(filename)

        return send_file(filename, mimetype="audio/mpeg", as_attachment=True, download_name="output.mp3")
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
