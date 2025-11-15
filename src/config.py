from dotenv import load_dotenv
import os

load_dotenv()

GROQ_CHAT_URL = os.getenv("GROQ_CHAT_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")


if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY não configurada. Verifique o arquivo .env")
