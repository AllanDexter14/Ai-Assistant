import json, os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000),
)

def index(request):
    return render(request, "assistant/index.html")

@require_POST
def ask(request):
    data = json.loads(request.body)
    prompt = data.get("prompt", "").strip()
    chat_history = data.get("history", [])
    if not prompt:
        return JsonResponse({"error": "Empty prompt"}, status=400)

    contents = []
    for m in chat_history[-20:]:
        role = "user" if m.get("role") == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m.get("text", "")}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    models = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
    for model in models:
        for attempt in range(2):
            try:
                res = client.models.generate_content(
                    model=model,
                    contents=contents,
                )
                return JsonResponse({"reply": res.text})
            except Exception as e:
                print("GEMINI ERROR:", model, repr(e))
                if "503" in str(e) or "429" in str(e):
                    time.sleep(1.5)
                    continue
                break
    return JsonResponse({"error": "The AI is busy right now, try again in a bit."}, status=503)