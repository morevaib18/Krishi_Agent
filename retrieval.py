"""
🌾 Retrieval layer for Krishi AI Support Agent

Implements:
- loading agricultural knowledge base (crop, disease, schemes)
- chunking
- embeddings
- FAISS vector store
- semantic search
- graceful fallback
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Any

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from config import (
    KB_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    RETRIEVAL_TOP_K,
    retrieval_ready,
)


# ============================================================
# 🌾 LOAD KNOWLEDGE BASE
# ============================================================

def load_knowledge_documents() -> List[Document]:
    """
    Load agricultural knowledge files such as:
    - crop information
    - disease management
    - government schemes
    """
    docs: List[Document] = []

    for path in sorted(KB_DIR.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue

        text = path.read_text(encoding="utf-8")

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": path.name,
                    "type": detect_doc_type(path.name),
                },
            )
        )

    return docs


# ============================================================
# 🧠 DOCUMENT TYPE DETECTION
# ============================================================

def detect_doc_type(filename: str) -> str:
    name = filename.lower()

    if "crop" in name:
        return "crop"
    if "disease" in name:
        return "disease"
    if "scheme" in name:
        return "scheme"

    return "general"


# ============================================================
# ✂️ CHUNKING
# ============================================================

def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks for better retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


# ============================================================
# 📦 VECTOR STORE
# ============================================================

@lru_cache(maxsize=1)
def build_vectorstore():
    """
    Build FAISS vector store (cached).
    """
    if not retrieval_ready():
        return None

    raw_docs = load_knowledge_documents()
    if not raw_docs:
        return None

    chunks = chunk_documents(raw_docs)

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


# ============================================================
# 🔍 RETRIEVE CONTEXT
# ============================================================

def retrieve_context(query: str, k: int = RETRIEVAL_TOP_K) -> Dict[str, Any]:
    """
    Retrieve top-k relevant agricultural knowledge.
    """

    result = {
        "used": False,
        "sources": [],
        "snippets": [],
        "context": "",
        "error": None,
    }

    try:
        vectorstore = build_vectorstore()

        if vectorstore is None:
            result["error"] = "Retrieval unavailable"
            return result

        docs = vectorstore.similarity_search(query, k=k)

        if not docs:
            result["error"] = "No relevant knowledge found"
            return result

        snippets = []
        sources = []

        for doc in docs:
            source = doc.metadata.get("source", "unknown")
            text = doc.page_content.strip()

            snippet = text[:500].strip()

            snippets.append(snippet)
            sources.append(source)

        joined_context = "\n\n".join(
            [f"[Source: {src}]\n{snip}" for src, snip in zip(sources, snippets)]
        )

        result["used"] = True
        #result["sources"] = sources
        result["sources"] = [
            d.metadata.get("source")
            for d in docs
        ]
        result["snippets"] = snippets
        #result["context"] = joined_context
        result["context"] = "\n\n".join(
            d.page_content for d in docs
        )

        return result

    except Exception as e:
        result["error"] = f"Retrieval error: {str(e)}"
        return result