import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Configure Flask App
app = Flask(__name__, static_folder='assets', static_url_path='/assets')

# 3. Configure API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in .env file!")

genai.configure(api_key=api_key)

# 4. System Prompt (AI Persona Settings)
# İsim burada düzeltildi: CureAI
SYSTEM_PROMPT = """
You are 'CureAI', a helpful and empathetic AI health assistant.
Your Goal: Provide simple, non-prescription remedies, herbal suggestions, and lifestyle advice based on user symptoms.

Rules:
1. LANGUAGE: Always respond in the SAME LANGUAGE as the user's message. (If user speaks Turkish, reply in Turkish. If English, reply in English).
2. NEVER provide a definitive medical diagnosis (e.g., do not say "You have cancer").
3. ALWAYS add a disclaimer: "This is not medical advice, please consult a doctor." (Translate this to the user's language).
4. Suggest only over-the-counter (OTC) remedies (like Paracetamol), vitamins, or natural home remedies.
5. For serious symptoms (chest pain, difficulty breathing), explicitly advise calling emergency services immediately.
"""

# 5. Select Model (Switched back to FLASH due to quota)
# Gemini 2.5 Flash hem hızlıdır hem de ücretsiz kotası geniştir.
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_ai():
    try:
        user_data = request.json
        user_message = user_data.get('message')

        if not user_message:
            return jsonify({"response": "Please enter a symptom."})

        response = model.generate_content(user_message)
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)