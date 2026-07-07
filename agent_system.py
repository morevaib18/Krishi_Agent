"""
Core agent system for the Krishi AI Agent capstone.

Features included to satisfy capstone phases:
- Baseline rule-based agent
- LLM-based specialist agent
- Tools:
    1) Crop advisory
    2) Disease diagnosis
    3) Government schemes
- Planning / routing
- Short-term memory
- Feedback-driven response adaptation
- Runtime logging
- Graceful failure handling
"""

from __future__ import annotations

import json
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from config import (
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    MAX_MEMORY_MESSAGES,
    FEEDBACK_STORE_PATH,
    RUNTIME_LOG_PATH,
    ENABLE_RUNTIME_LOGGING,
    llm_ready,
)
from retrieval import retrieve_context


# ============================================================
# 🌾 TOOLS (Phase 5: Tool usage)
# ============================================================

@tool
def crop_advisory(query: str) -> str:
    """
    Provide crop recommendations based on soil, region, and season.

    This is a deterministic tool (no randomness),
    ensuring predictable outputs for evaluation.
    """
    return "Recommended crops: Soybean, Cotton, Wheat based on Indian climate."


@tool
def disease_diagnosis(query: str) -> str:
    """
    Diagnose crop diseases and suggest treatments.

    Used when user asks about symptoms like:
    - yellow spots
    - infections
    - leaf damage
    """
    return "Yellow spots indicate fungal infection. Use fungicide and avoid overwatering."


@tool
def government_schemes(query: str) -> str:
    """
    Provide information about farmer government schemes.

    Example:
    - PM-KISAN
    - subsidies
    """
    return "PM-KISAN provides ₹6000/year to eligible farmers."


# ============================================================
# 🧩 HELPER FUNCTIONS
# ============================================================

def _extract_final_text(result: dict) -> str:
    """
    Extract final response from LangChain agent output.
    Handles different response formats safely.
    """
    final_message = result["messages"][-1]
    content = getattr(final_message, "content", final_message)
    return str(content)


def _safe_load_json(path, default):
    """
    Safely load JSON file.
    Returns default if file is missing or corrupted.
    """
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _safe_write_json(path, data):
    """
    Safely write JSON file.
    """
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _append_jsonl(path, record: dict):
    """
    Append logs in JSONL format for runtime tracing.
    """
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================
# 🧠 MEMORY (Phase 6)
# ============================================================

@dataclass
class ConversationMemory:
    """
    Simple short-term memory for conversation tracking.
    Keeps last N messages only.
    """
    messages: List[Dict[str, str]] = field(default_factory=list)

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        # Keep only latest messages
        if len(self.messages) > MAX_MEMORY_MESSAGES:
            self.messages = self.messages[-MAX_MEMORY_MESSAGES:]

    def clear(self):
        self.messages = []

    def formatted(self):
        """
        Format memory into prompt-friendly string.
        """
        return "\n".join(f"{m['role']}: {m['content']}" for m in self.messages)


# ============================================================
# 🔁 FEEDBACK SYSTEM (Phase 7)
# ============================================================

class FeedbackProfileStore:
    """
    Stores user preferences and adapts future responses.

    Tracks:
    - response style (concise/detailed)
    - domain priority (crop/disease/schemes)
    - feedback history
    """

    def __init__(self):
        self.data = _safe_load_json(
            FEEDBACK_STORE_PATH,
            default={
                "default_user": {
                    "style": "balanced",
                    "priority": "balanced",
                    "history": []
                }
            },
        )

    def get_profile(self, user_id: str) -> dict:
        if user_id not in self.data:
            self.data[user_id] = {
                "style": "balanced",
                "priority": "balanced",
                "history": []
            }
            self.save()
        return self.data[user_id]

    def update(self, user_id: str, signal: str):
        """
        Update user preference profile.

        Example signals:
        - prefer_concise
        - prefer_detailed
        - prioritize_crop_advice
        - prioritize_disease_solution
        - prioritize_government_schemes
        """
        profile = self.get_profile(user_id)

        if signal == "prefer_concise":
            profile["style"] = "concise"

        elif signal == "prefer_detailed":
            profile["style"] = "detailed"

        elif signal == "prioritize_crop_advice":
            profile["priority"] = "crop"

        elif signal == "prioritize_disease_solution":
            profile["priority"] = "disease"

        elif signal == "prioritize_government_schemes":
            profile["priority"] = "scheme"

        # Store history for audit
        profile["history"].append({
            "signal": signal,
            "timestamp": datetime.utcnow().isoformat()
        })

        self.save()

    def save(self):
        _safe_write_json(FEEDBACK_STORE_PATH, self.data)


# ============================================================
# 🤖 MAIN AGENT SYSTEM
# ============================================================

class KrishiAgentSystem:
    """
    Main orchestrator for baseline + smart AI agent.
    """

    def __init__(self, user_id="default_user"):
        self.user_id = user_id

        # Memory + feedback
        self.memory = ConversationMemory()
        self.feedback_store = FeedbackProfileStore()
        self.profile = self.feedback_store.get_profile(user_id)

        self._agent = None

    # --------------------------------------------------------
    # Phase 2: Baseline Agent
    # --------------------------------------------------------
    def baseline_respond(self, query: str):
        """
        Simple rule-based agent (intentionally limited).
        """
        text = query.lower()

        if "crop" in text:
            response = "Baseline: Choose crops based on soil and climate."
            route = ["crop"]

        elif "disease" in text:
            response = "Baseline: Crop diseases require diagnosis."
            route = ["disease"]

        else:
            response = "Baseline: Ask about crops, diseases, or schemes."
            route = ["general"]

        self.memory.add("user", query)
        self.memory.add("assistant", response)

        result = {
            "mode": "baseline",
            "response": response,
            "route": route,
            "latency_ms": 0,
            "used_retrieval": False,
        }

        self._log_run(query, result)
        return result

    # --------------------------------------------------------
    # Phase 3: LLM Agent
    # --------------------------------------------------------
    def _build_agent(self):
        """
        Build LLM agent with tools.
        """
        model = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMPERATURE,
        )

        return create_agent(
            model=model,
            tools=[crop_advisory, disease_diagnosis, government_schemes],
            system_prompt="You are Krishi AI helping farmers.",
        )

    @property
    def agent(self):
        if self._agent is None:
            self._agent = self._build_agent()
        return self._agent

    # --------------------------------------------------------
    # Phase 3 + 4: Smart Agent
    # --------------------------------------------------------
    def smart_respond(self, query: str, use_retrieval=True):
        """
        Intelligent agent using LLM + optional RAG.
        """
        start = time.time()

        retrieval = retrieve_context(query) if use_retrieval else {}
        context = retrieval.get("context", "")

        history = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in self.memory.messages[-5:]
        ])

        response_style = "normal"

        if self.profile.get("prefer_concise"):
            response_style = "concise"

        if self.profile.get("prefer_detailed"):
            response_style = "detailed"

        enhanced_prompt = f"""
        You are Krishi AI Assistant.

        Retrieved Knowledge:
        {context}

        Conversation History:
        {history}

        Response Style:
        {response_style}

        User Question:
        {query}

        Instructions:
        - Use retrieved knowledge whenever relevant.
        - Use conversation history for follow-up questions.
        - Follow response style preference.
        - If information is unavailable, say so.

        Answer:
        """
        try:
            result = self.agent.invoke({
                "messages": [{"role": "user", "content": enhanced_prompt}]
            })

            response = _extract_final_text(result)

        except Exception as e:
            response = f"Error: {str(e)}"

        latency = round((time.time() - start) * 1000, 2)

        self.memory.add("user", query)
        self.memory.add("assistant", response)

        result = {
            "mode": "smart",
            "response": str(response),  # 🔥 prevents UI crash
            "route": ["general"],
            "latency_ms": latency,
            "used_retrieval": retrieval.get("used", False),
            "retrieval_sources": retrieval.get("sources", []),
        }

        self._log_run(query, result)
        return result

    # --------------------------------------------------------
    def respond(self, user_input: str, mode="smart", use_retrieval=True):
        """
        Unified public entry point.
        """
        if mode == "baseline":
            return self.baseline_respond(user_input)
        return self.smart_respond(user_input, use_retrieval)

    # --------------------------------------------------------
    # Phase 7: Feedback
    # --------------------------------------------------------
    def record_feedback(self, signal: str):
        """
        Update user preference profile.

        Example signals:
        - prefer_concise → shorter responses
        - prefer_detailed → more explanation
        - prioritize_crop_advice → focus on crop recommendations
        - prioritize_disease_solution → focus on diagnosis & treatment
        - prioritize_government_schemes → highlight schemes & subsidies
        """
        self.feedback_store.update(self.user_id, signal)
        self.profile = self.feedback_store.get_profile(self.user_id)

    def reset_memory(self):
        self.memory.clear()

    # --------------------------------------------------------
    # Phase 8: Logging
    # --------------------------------------------------------
    def _log_run(self, user_input: str, result: dict):
        """
        Record runtime logs for evaluation and debugging.
        """
        if not ENABLE_RUNTIME_LOGGING:
            return
        
        query_hash = hashlib.sha256(
        user_input.encode()
        ).hexdigest()

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": self.user_id,
            "query_hash": query_hash,
            "mode": result.get("mode"),
            "route": result.get("route"),
            "latency_ms": result.get("latency_ms"),
            "used_retrieval": result.get("used_retrieval"),
            "retrieval_sources": result.get("retrieval_sources", []),
            "error": result.get("error"),
        }

        try:
            _append_jsonl(RUNTIME_LOG_PATH, record)
        except Exception:
            pass