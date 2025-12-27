import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("HATA: API Anahtarı bulunamadı!")
else:
    genai.configure(api_key=api_key)
    print("API Anahtarı bulundu, modeller listeleniyor...\n")
    
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Kullanılabilir Model: {m.name}")
    except Exception as e:
        print(f"HATA OLUŞTU: {e}")