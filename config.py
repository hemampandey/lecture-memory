import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

load_dotenv()

class Config:
    # --- Project Paths ---
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    
    # Ensure directories exist
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # --- Model Settings ---
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "tiny")
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL = "gpt-4o-mini"
    
    # --- Qdrant Settings ---
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_URL: Optional[str] = os.getenv("QDRANT_URL")  # Use this for Qdrant Cloud
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME = "lecture_memory"

    # --- API Settings ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

config = Config()
