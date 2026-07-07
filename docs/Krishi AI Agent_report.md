# 🌾 Krishi AI Agent – Capstone Report

## 📌 Project Summary

Krishi AI Agent is a multi-capability AI assistant designed to support farmers with agricultural decision-making. The agent provides crop recommendations, disease diagnosis support, government scheme information, and farming best practices through a conversational interface.

The solution combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), intelligent tool usage, memory, and adaptive feedback to deliver practical and contextual guidance.

### 🎯 Key Capabilities

* 🌱 Crop Recommendations
* 🦠 Disease Diagnosis Support
*  🏛 Government Scheme Guidance
* 🌾 Farming Best Practices
* 🧠 Conversational Memory
* 📚 Knowledge Retrieval (RAG)
* 🔄 Adaptive Responses

---

# 🌱 Phase 1: Understand the Problem & Define Success

## 👤 Primary User Persona

### Farmers

* Small-scale farmers
* Medium-scale farmers
* Rural users
* Users with limited technical expertise

### User Needs

* Quick agricultural advice
* Reliable recommendations
* Easy-to-understand explanations
* Government scheme awareness

---

## 🎯 Problem Statement

Farmers often struggle to access:

* Immediate expert guidance
* Reliable crop recommendations
* Accurate disease diagnosis
* Government support information

### Current Challenges

❌ Generic advice

❌ Limited accessibility

❌ Poor contextual understanding

❌ Non-interactive systems

---

## 📥 Inputs

* Crop-related questions
* Disease symptoms
* Farming queries
* Government scheme questions
* Optional location information

---

## 📤 Outputs

* Crop recommendations
* Disease diagnosis suggestions
* Treatment guidance
* Government scheme information
* Best farming practices

---

## ⚠️ Constraints

* Limited knowledge base
* No real-time market APIs
* Dependence on LLM services
* Basic user interface

---

## 🔍 Assumptions

* Users provide understandable queries
* Knowledge base covers common scenarios
* Responses are used for advisory purposes

---

## 💬 Example Questions

* Which crop is best for Maharashtra?
* My crop has yellow spots. What should I do?
* What schemes are available for farmers?
* How can I improve soil fertility?

---

## ✅ Success Criteria

* Correct tool selection
* Accurate responses
* Context retention
* Retrieval-enhanced answers
* Improved user experience

---

## ❌ Failure Cases

* Missing API key
* Ambiguous user queries
* Missing knowledge base information
* Tool selection errors
* Invalid inputs

---

# 🤖 Phase 2: Build a Basic Working Agent

## 🧱 Baseline Agent

Initial implementation used:

* Rule-based logic
* Static templates
* Hardcoded responses

### ⚠️ Limitations

* No reasoning capability
* No personalization
* No contextual awareness
* No adaptability

### ❗ Why Baseline Was Insufficient

Farmers require:

* Context-aware recommendations
* Personalized assistance
* Domain-specific knowledge
* Follow-up conversation support

---

# 🧠 Phase 3: Make the Agent Smarter

## 🔌 LLM Integration

The system integrates an LLM to provide:

* Natural language understanding
* Context-aware responses
* Better explanations
* Flexible interaction

---

## 🧪 Prompt Engineering Strategy

### Prompt A

Generic prompt

### Prompt B

Role-based agricultural assistant

### Prompt C ✅ Selected

Structured prompt including:

* Retrieved knowledge
* Conversation history
* User preferences
* Safety instructions

---

## 📊 Prompt Comparison

| Prompt | Characteristics               | Result              |
| ------ | ----------------------------- | ------------------- |
| A      | Generic                       | Basic responses     |
| B      | Role-based                    | Better explanations |
| C      | Retrieval + Memory + Feedback | Best performance    |

---

## ✅ Improvements Achieved

* Better reasoning
* More relevant responses
* Reduced hallucinations
* Improved contextual understanding

---

## ⚠️ New Failure Modes

* API dependency
* Hallucination risk
* Prompt sensitivity
* Response verbosity

---

# 📚 Phase 4: Add Knowledge & Retrieval (RAG)

## 📂 Knowledge Base

Stored under:

```text
data/knowledge_base/
```

---

## 🔍 Retrieval Workflow

1. Load documents
2. Split documents into chunks
3. Generate embeddings
4. Store vectors in FAISS
5. Retrieve relevant content
6. Inject retrieved context into prompt
7. Generate grounded response

---

## 🚀 Benefits

* Context-aware answers
* Reduced hallucinations
* Domain-specific responses
* Better factual grounding

---

## 📊 Without vs With Retrieval

| Scenario    | Result               |
| ----------- | -------------------- |
| Without RAG | Generic responses    |
| With RAG    | Contextual responses |

---

## ⚠️ Missing Data Handling

If retrieval fails:

* Falls back to LLM reasoning
* No application crash
* User informed appropriately

---

# 🛠 Phase 5: Enable Tool Usage

## 🔧 Tools Implemented

### 🌱 Crop Advisory Tool

Provides crop recommendations.

### 🦠 Disease Diagnosis Tool

Analyzes symptoms and suggests treatments.

### 🏛 Government Scheme Tool

Provides scheme eligibility and benefits.

---

## 🧠 Tool Routing

Agent dynamically selects tools based on:

* User intent
* Query classification
* Available knowledge

---

## 🛡 Safeguards

* Input validation
* Error handling
* Safe tool execution
* No recursive loops

---

## ❌ Failure Example

Invalid disease symptoms

Result:

Graceful error handling with guidance.

---

# 🧩 Phase 6: Planning, Memory & Context

## 🧠 Planning Workflow

1. Understand query
2. Check memory
3. Retrieve context
4. Select tool
5. Generate response

---

## 💾 Conversational Memory

Stores:

* Previous user questions
* Previous responses
* Recent conversation context

---

## 🔄 Benefits

* Better follow-up conversations
* Reduced repeated questions
* Improved user experience

---

## 📌 Example

User:
Which crop is suitable for Maharashtra?

Assistant:
Soybean and cotton are suitable options.

User:
What irrigation method should I use?

Assistant:
Drip irrigation is recommended for soybean cultivation.

---

# 🔁 Phase 7: Adaptive Behaviour & Feedback

## 📥 Feedback Options

Users can select:

* Prefer concise responses
* Prefer detailed responses

---

## 🔄 Adaptation Mechanism

Stored preferences influence future responses.

---

## 📊 Before vs After

| Before         | After               |
| -------------- | ------------------- |
| Generic answer | Personalized answer |

---

## ✅ Benefits

* Better personalization
* Improved usability
* Higher user satisfaction

---

# 🚀 Phase 8: Deployment Readiness

## 📦 Packaging

Project includes:

* requirements.txt
* Dockerfile
* .env configuration

---

## 📊 Monitoring & Logging

Tracks:

* Response latency
* Tool usage
* Retrieval success
* Errors

---

## 🔒 Privacy Improvements

* Raw queries not stored
* Query hashes logged
* User data minimized

---

## ⚠️ Failure Handling

* Graceful fallback
* Friendly error messages
* System resilience

---

## 🌐 Deployment Targets

* Local deployment
* Docker containers
* Hugging Face Spaces

---

# 📊 Phase 9: Evaluation & Engineering Review

## 🧪 Evaluation Categories

### 📚 Retrieval Accuracy

Measures grounding quality.

### 🔧 Tool Selection Accuracy

Measures routing correctness.

### 🧠 Memory Retention

Measures context awareness.

### 🔄 Feedback Adaptation

Measures personalization.

### 🛡 Safety Compliance

Measures safe behavior.

---

## 📏 Metrics

* Response relevance
* Tool accuracy
* Consistency
* Clarity
* Latency
* Safety score

---

## 🔍 Debugged Failure Case

### Problem

Retrieved knowledge was generated but not passed into the final prompt.

### Root Cause

RAG pipeline was disconnected from answer generation.

### Fix

Injected retrieved context directly into prompt construction.

### Before

Question:
What government scheme helps farmers?

Response:
Generic support information.

### After

Question:
What government scheme helps farmers?

Response:
PM-KISAN provides ₹6000 annually to eligible farmers.

### Outcome

✅ Improved grounding

✅ Better factual accuracy

✅ Stronger RAG performance

---

# ⚖️ Safety & Ethics

## Safety Principles

* Avoid harmful advice
* Encourage expert consultation
* Clearly communicate uncertainty
* Avoid misleading recommendations

---

## Governance Controls

* Privacy-aware logging
* Tool restrictions
* Evaluation monitoring
* Transparent limitations

---

# 🚀 Future Roadmap

* 🌐 Marathi Support
* 🌐 Hindi Support
* ☁ Weather API Integration
* 📈 Market Price APIs
* 🎤 Voice Assistant
* 👨‍🌾 Human Expert Escalation
* 📚 Expanded Knowledge Base
* 📊 Evaluation Dashboard

---

# 📎 Appendix

## Included Artifacts

* Architecture Diagram
* Evaluation Results
* Sample Logs
* Prompt Comparison Results
* Failure Analysis Evidence
* Deployment Screenshots

## Repository Structure

```text
app.py
agent_system.py
retrieval.py
evaluation.py
data/
knowledge_base/
logs/
README.md
Dockerfile
requirements.txt
```

---

## 🏁 Conclusion

Krishi AI Agent demonstrates how LLMs, Retrieval-Augmented Generation (RAG), intelligent tool usage, memory, and adaptive feedback can be combined to create a practical agricultural assistant. The system provides contextual, explainable, and farmer-friendly guidance while maintaining safety, transparency, and extensibility for future enhancements.
