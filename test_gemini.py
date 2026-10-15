import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)
key = os.getenv("GEMINI_API_KEY")
print("Key loaded:", bool(key), "| starts with:", key[:4] if key else None)

client = genai.Client(api_key=key)
try:
    res = client.models.generate_content(model="gemini-3.8-flash", contents="Say hi")
    print("REPLY:", res.text)
except Exception as e:
    print("ERROR:", repr(e))