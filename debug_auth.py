# debug_auth.py
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# load .env explicitly
load_dotenv(Path(__file__).resolve().parent / ".env")
k = os.getenv("OPENAI_API_KEY") or ""
print("Key prefix:", k[:10], "len:", len(k), "tail repr:", repr(k[-2:] if k else ""))

try:
    client = OpenAI()  # auto-reads OPENAI_API_KEY
    models = client.models.list()
    print("✅ Auth OK. Model count:", len(models.data))
except Exception as e:
    print("❌ Auth failed:", e)
