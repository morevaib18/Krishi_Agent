"""
🌾 Central configuration for Krishi AI Support Agent
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------------------------------------------------
# 📁 Paths
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
KB_DIR = DATA_DIR / "knowledge_base"
DOCS_DIR = BASE_DIR / "docs"

# Runtime-generated files
RUNTIME_LOG_PATH = DOCS_DIR / "runtime_logs.jsonl"
EVAL_RESULTS_PATH = DOCS_DIR / "evaluation_results.csv"
FEEDBACK_STORE_PATH = DATA_DIR / "user_feedback.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# 🌾 App Metadata
# ---------------------------------------------------
APP_TITLE = "Krishi AI Support Agent"
APP_ICON = "🌾"

# ---------------------------------------------------
# 🤖 Model / API Config
# ---------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Optional (if you later add web search)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# ---------------------------------------------------
# 📚 Retrieval Config (RAG)
# ---------------------------------------------------
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "700"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

# ---------------------------------------------------
# 🧠 Memory Config
# ---------------------------------------------------
MAX_MEMORY_MESSAGES = int(os.getenv("MAX_MEMORY_MESSAGES", "8"))

# ---------------------------------------------------
# 📊 Logging
# ---------------------------------------------------
ENABLE_RUNTIME_LOGGING = os.getenv("ENABLE_RUNTIME_LOGGING", "true").lower() == "true"

# ---------------------------------------------------
# 🔧 Helper Functions
# ---------------------------------------------------

def llm_ready() -> bool:
    """Check if LLM is ready."""
    return bool(OPENAI_API_KEY)


def tavily_ready() -> bool:
    """Check if Tavily (web search) is configured."""
    return bool(TAVILY_API_KEY)


def retrieval_ready() -> bool:
    """Check if embeddings can be used."""
    return bool(OPENAI_API_KEY)


def missing_runtime_vars() -> list[str]:
    """Return missing environment variables (for UI display)."""
    missing = []

    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    if not TAVILY_API_KEY:
        missing.append("TAVILY_API_KEY")

    return missing