# 🎙️ AI Voice Chat Web App  
![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)  
Real-time voice and text chat using Flask, Socket.IO, SpeechRecognition, and gTTS.

---

## ✨ Overview

This AI-powered web application allows users to:
- 💬 Chat with text messages
- 🎤 Speak and convert voice to text (Speech-to-Text)
- 🔊 Convert typed messages to voice responses (Text-to-Speech)
- ⚡ Communicate in real-time using WebSockets (Socket.IO)

Everything runs directly in the browser — no external app needed.

---

## 🚀 Features

✅ Real-time AI-style chat interface  
✅ Voice-to-text transcription using `SpeechRecognition`  
✅ Text-to-speech conversion using `gTTS`  
✅ WebSocket-based instant communication  
✅ Stylish chat bubbles with audio player  
✅ 🎧 Works in most modern browsers  

---

## 📸 Demo

>![image](https://github.com/user-attachments/assets/8f848e9d-13b9-4002-a725-3f6e9835d3da)


---

## 🛠️ Tech Stack

| Layer         | Technology                |
|---------------|---------------------------|
| **Backend**   | Flask, Flask-SocketIO     |
| **Frontend**  | HTML, CSS, JavaScript     |
| **Voice APIs**| SpeechRecognition, gTTS   |
| **WebSocket** | Socket.IO                 |

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/flask-voice-chat.git
cd flask-voice-chat
python -m venv venv
# Activate:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
##Run
python app.py
