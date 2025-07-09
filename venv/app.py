from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o"  # kamu juga bisa ganti dengan model lain dari openrouter.ai

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",  # WAJIB di OpenRouter
        "X-Title": "FlaskChatbot"                # Nama bebas, wajib diisi
    }

    payload = {
    "model": MODEL,
    "max_tokens": 1024,  # Tambahkan ini agar tidak over-limit
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]
}


    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        print("ERROR:", e)
        print("FULL RESPON:", response.text)
        reply = "Maaf, terjadi kesalahan."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
