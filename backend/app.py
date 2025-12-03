from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "AIzaSyBPpf1Yc7uyrseh9dlKJlG8OuZ1m7KlhVc"  # Replace this
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def generate_response(user_input):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": user_input}]}
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.HTTPError as http_err:
        print("Gemini API HTTP Error:", http_err)
        print("Response:", response.text)
        return "Error contacting Gemini API."
    except Exception as err:
        print("Other Error:", err)
        return "Something went wrong."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    reply = generate_response(user_input)
    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
