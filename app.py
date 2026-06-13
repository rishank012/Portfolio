import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load the hidden environment variables locally
load_dotenv()

app = Flask(__name__)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Routes to serve your existing HTML pages ---
@app.route('/')
@app.route('/portfolio.html')
def home():
    return render_template('portfolio.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/skills.html')
def skills():
    return render_template('skills.html')

@app.route('/projects.html')
def projects():
    return render_template('projects.html')

@app.route('/certificates.html')
def certificates():
    return render_template('certificates.html')

# --- Secure Chatbot API Route ---
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    
    # We define the system prompt securely on the backend
    system_instruction = {
        "parts": {
            "text": "You are Edith, the AI portfolio assistant for Rishank Rastogi. Rishank is a B.Tech CSE student at shobhit University meerut specializing in Python, Ai and Machine Learning, and Web Frameworks. His achivemnets is that he is the winner of internal Smart India Hackathon 2025 and He got a certificate of excellence in Machine Learning that is conducted by Summer Analytics 2025 in associatin with IIT Guwati. His major projects include a 'Vehicle Price Intelligence System' (using KNN and Decision Trees), a 'Real-Time Dynamic Pricing System' built in collaboration with IIT Guwahati and pahtway, An Ai Portfolio Maker and his 'Friday AI Assistant'. And if anyone wants to know more about his projects you can tell them to visit his project section. If anyone ask you about his resume, you can tell them to download it from the top right corner button that have 'Resume' written on it. If anyone ask you about his achivements and certification, you can tell about his achivements as described or you can tell them to visit his certificates section. Also he is skilled in Python, HTML, CSS, JS, Pandas, Numpy, Scikit-learn, Tensorflow, etc. You can tell the user to visit his skill section to know more about Rishank's skills. Answer questions politely, briefly, and professionally. Do not answer questions unrelated to Rishank's portfolio, skills, or background. And Don't use any bold, itelics, or any other type to describe your message keep it like a normal ai assistant"
        }
    }
    
    payload = {
        "system_instruction": system_instruction,
        "contents": data.get("contents", [])
    }
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={GEMINI_API_KEY}"
    
    try:
        response = requests.post(url, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)