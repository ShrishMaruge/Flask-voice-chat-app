from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import uuid
import time
import threading
import speech_recognition as sr
from gtts import gTTS

# App configuration
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'wav'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility: Check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Utility: Clean up old files
def cleanup_uploads(folder, max_age_seconds=3600):
    while True:
        now = time.time()
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            if os.path.isfile(path) and now - os.path.getmtime(path) > max_age_seconds:
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Cleanup error: {e}")
        time.sleep(1800)  # Clean every 30 minutes

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_uploads, args=(UPLOAD_FOLDER,), daemon=True)
cleanup_thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/uploads/<filename>")
def get_audio(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/upload_voice", methods=["POST"])
def upload_voice():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Only WAV supported."}), 400

    file_name = f"{uuid.uuid4()}.wav"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    file.save(file_path)

    # Speech recognition
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Could not understand audio"
    except sr.RequestError:
        text = "Speech recognition service unavailable"
    except Exception as e:
        text = f"Error processing audio: {str(e)}"

    return jsonify({"text": text, "audio": f"/uploads/{file_name}"})

# SocketIO - Text to Speech
@socketio.on("send_text", namespace="/chat")
def handle_text_message(data):
    text = data.get("text", "").strip()
    if not text:
        socketio.emit("receive_message", {"error": "Empty text input"}, namespace="/chat")
        return

    file_name = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    try:
        tts = gTTS(text)
        tts.save(file_path)
        socketio.emit("receive_message", {"text": text, "audio": f"/uploads/{file_name}"}, namespace="/chat")
    except Exception as e:
        socketio.emit("receive_message", {"error": f"TTS Error: {str(e)}"}, namespace="/chat")

if __name__ == "__main__":
    socketio.run(app, debug=True)
