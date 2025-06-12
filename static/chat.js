// Connect to Socket.IO namespace "/chat"
const socket = io("/chat");

// Append messages to chat box
function addMessage(sender, text, audioUrl = null) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender === "You" ? "user" : "bot");

    const timestamp = new Date().toLocaleTimeString();
    msgDiv.innerHTML = `<strong>${sender} (${timestamp}):</strong> ${text}`;

    if (audioUrl) {
        const audio = document.createElement("audio");
        audio.controls = true;
        audio.src = audioUrl;
        msgDiv.appendChild(audio);
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Handle messages from server
socket.on("receive_message", data => {
    if (data.error) {
        addMessage("Bot", `❌ ${data.error}`);
    } else {
        addMessage("Bot", data.text, data.audio);
    }
});

// Send text message
function sendMessage() {
    const input = document.getElementById("message");
    const msg = input.value.trim();
    if (!msg) return;

    addMessage("You", msg);
    socket.emit("send_text", { text: msg });
    input.value = "";
}

// Record audio and upload
function recordAudio() {
    const micButton = document.getElementById("mic-button");
    micButton.disabled = true;
    micButton.innerText = "⏳ Listening...";

    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        const chunks = [];

        mediaRecorder.ondataavailable = e => chunks.push(e.data);

        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append("file", blob, "recording.wav");

            fetch("/upload_voice", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    addMessage("Bot", `❌ ${data.error}`);
                } else {
                    addMessage("You (Voice)", "(Voice message)", data.audio);
                    addMessage("Bot", data.text);
                }
            })
            .catch(err => {
                addMessage("Bot", "❌ Upload failed. Try again.");
                console.error(err);
            })
            .finally(() => {
                micButton.disabled = false;
                micButton.innerText = "🎤 Speak";
            });
        };

        mediaRecorder.start();
        setTimeout(() => {
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop());
        }, 5000); // 5 seconds recording
    }).catch(err => {
        console.error("Mic access denied:", err);
        addMessage("Bot", "❌ Microphone access denied.");
        micButton.disabled = false;
        micButton.innerText = "🎤 Speak";
    });
}
