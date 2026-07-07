"""
🌾 Krishi AI Support Agent (Streamlit UI)
Based on original multi-agent structure
"""
from __future__ import annotations

import streamlit as st

from config import APP_TITLE, APP_ICON, missing_runtime_vars
from agent_system import KrishiAgentSystem


# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
)

st.title(f"{APP_ICON} {APP_TITLE}")
st.caption("🌾 AI-powered farmer support assistant for crops, diseases, and government schemes.")


# -------------------------------------------------
# Session State
# -------------------------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = KrishiAgentSystem(user_id="streamlit_user")

if "last_result" not in st.session_state:
    st.session_state.last_result = None


agent: KrishiAgentSystem = st.session_state.agent


# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    mode = st.radio(
        "Agent mode",
        options=["smart", "baseline"],
        index=0,
        help="Use baseline for simple responses or smart for full AI agent.",
    )

    use_retrieval = st.checkbox(
        "Use knowledge base",
        value=True,
        help="Enable retrieval for better answers.",
    )

    st.subheader("🧠 Feedback")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Concise"):
            agent.record_feedback("prefer_concise")
            st.success("Saved: concise")
    with col2:
        if st.button("Detailed"):
            agent.record_feedback("prefer_detailed")
            st.success("Saved: detailed")

    if st.button("Reset Memory"):
        agent.reset_memory()
        st.success("Memory cleared")

    st.subheader("💡 Example Questions")
    st.markdown(
        """
- Which crop is best for Maharashtra?
- My crop has yellow spots, what should I do?
- What government schemes are available?
- How to improve soil fertility?
"""
    )

    missing = missing_runtime_vars()
    if mode == "smart" and missing:
        st.warning("Missing API keys:\n\n" + "\n".join(f"- {m}" for m in missing))


# -------------------------------------------------
# Chat History
# -------------------------------------------------
for msg in agent.memory.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -------------------------------------------------
# User Input
# -------------------------------------------------
prompt = st.chat_input("Ask your farming question...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🌱 Thinking..."):

            try:
                result = agent.respond(
                    user_input=prompt,
                    mode=mode,
                    use_retrieval=use_retrieval if mode == "smart" else False,
                )

                # 🔥 CRITICAL FIX (prevents your HF error)
                response_text = result["response"] if isinstance(result, dict) else str(result)

                st.markdown(response_text)

                # Debug section
                with st.expander("🔍 Debug Info"):
                    st.write("Mode:", result.get("mode"))
                    st.write("Route:", result.get("route"))
                    st.write("Latency (ms):", result.get("latency_ms"))
                    st.write("Used retrieval:", result.get("used_retrieval"))
                    st.write("Sources:", result.get("retrieval_sources"))
                    st.write("Error:", result.get("error"))
                    st.write("Retrieved Sources:")
                    st.write(result.get("retrieval_sources"))
                    st.write("Memory Size:")
                    st.write(len(agent.memory.messages))

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

    st.session_state.last_result = result