import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def explain_medical_text(text):
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # or whichever model available
        contents=text
    )
    return response.text
