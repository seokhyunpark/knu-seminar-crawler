import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_response(data):
    try:
        if data.startswith("SITE"):
            prompt = os.getenv("AI_PROMPT")
            response = model.generate_content(data + prompt)
            return response.text
        return None
    except Exception as e:
        print("[ERROR] generate_response: ", e)
        return None
