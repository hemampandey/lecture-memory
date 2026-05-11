"""
Use this as a diagnostic tool
RUN: python main.py
"""


import sys
from config import config
from logger import logger
from qdrant_client import QdrantClient

def check_system():
    """Verify that the environment is ready for Lecture Memory."""
    logger.info("🚦 Starting System Diagnostic...")
    
    # 1. Check Qdrant
    try:
        if config.QDRANT_URL:
            client = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)
            logger.info(f"✅ Qdrant Cloud: {config.QDRANT_URL}")
        else:
            client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
            logger.info(f"✅ Qdrant Local: {config.QDRANT_HOST}:{config.QDRANT_PORT}")
        
        client.get_collections()
    except Exception as e:
        logger.error(f"❌ Qdrant Connection: FAILED. Ensure Docker is running. Error: {e}")

    # 2. Check OpenAI / API
    if config.OPENAI_API_KEY and len(config.OPENAI_API_KEY) > 10:
        logger.info("✅ API Key: CONFIGURED")
    else:
        logger.warning("⚠️ API Key: MISSING or INVALID in .env")

    # 3. Check Folders
    if config.RAW_DATA_DIR.exists():
        logger.info(f"✅ Data Directory: READY ({config.RAW_DATA_DIR})")
    else:
        config.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("✅ Data Directory: CREATED")

    logger.info("--- Diagnostic Complete ---")
    print("\nTo start the UI, run:  uv run streamlit run ui/app.py")
    print("To ingest data, run:   uv run python ingest.py --url <URL> --session <N>\n")

if __name__ == "__main__":
    check_system()
