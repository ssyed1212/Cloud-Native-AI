import os
from pathlib import Path

from dotenv import load_dotenv

# load .env from the lab root so it works with the lab's expected layout
# (lab7-database/.env)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path, override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "").strip()
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
