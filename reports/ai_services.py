import os
from google import genai
from dotenv import load_dotenv

# Load env from .env if present
load_dotenv()

SYSTEM_PROMPT = """
You are a medical assistant.
Explain the medical report in simple language.
Highlight abnormal values.
Give lifestyle suggestions.
Do not provide diagnosis or prescriptions.
Structure response as:

SUMMARY:
ABNORMAL FINDINGS:
LIFESTYLE SUGGESTIONS:
"""


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Set it in the environment or .env file."
        )
    return genai.Client(api_key=api_key)


def analyze_report(text: str) -> str:
    client = _get_client()
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=SYSTEM_PROMPT + "\n\n" + text,
    )
    return getattr(response, "text", str(response))
