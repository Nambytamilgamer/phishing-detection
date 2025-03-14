from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def analyze_text(text):
    prompt = f"Analyze this message and determine if it is a phishing attempt. Reply with only 'Phishing' or 'Not Phishing':\n{text}"
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip() if response else "Error: No response from AI"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    result = analyze_text(text)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
