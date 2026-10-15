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
    prompt = json.loads(request.body).get("prompt", "").strip()
    if not prompt:
        return JsonResponse({"error": "Empty prompt"}, status=400)
    try:
        res = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
        return JsonResponse({"reply": res.text})
    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        return JsonResponse({"error": "Something went wrong"}, status=500)