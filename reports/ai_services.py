import os
from google import genai
from dotenv import load_dotenv

# Load env from .env if present
load_dotenv()

SYSTEM_PROMPT = """
You are a highly experienced medical assistant AI.
Your goal is to explain complex medical reports to patients in clear, understandable, and reassuring language.
Provide detailed explanations for medical terms.
Use Markdown formatting to make the text easy to read (bullet points, bold text for key terms).

Structure your response strictly as follows:

SUMMARY:
(Provide a comprehensive summary of the report. Explain what the test is for. Use bullet points if multiple tests were done.)

ABNORMAL FINDINGS:
(List any values that are out of range. Explain what "High" or "Low" means in this context. Use bold text for the specific result e.g., **Hemoglobin**.)

LIFESTYLE SUGGESTIONS:
(Provide actionable, healthy lifestyle tips relevant to the findings. Use bullet points.)
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
