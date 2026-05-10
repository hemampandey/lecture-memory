# 🎓 Lecture Memory: Technical Walkthrough

This guide explains how the system works from the inside out. Use this to prepare for technical interviews and to master the codebase.

---

## 🏗️ High-Level Architecture

The system is split into two main pipelines:

### 📥 Ingestion Pipeline
1. **YouTube Download**: `yt-dlp` extracts the audio.
2. **Whisper Transcription**: The audio is turned into text segments with timestamps.
3. **Semantic Chunking**: Small segments are merged into ~75-second "chunks" to provide enough context for the LLM.
4. **LLM Tagging**: Each chunk is analyzed to extract a "Topic" and "Keywords".
5. **Vector Embedding**: Text is converted into numbers (vectors) using `all-MiniLM-L6-v2`.
6. **Qdrant Storage**: Vectors and metadata are stored in the local vector database.

### 🔍 Retrieval Pipeline (The Agent)
1. **User Query**: You ask a question in the UI.
2. **LangGraph Agent**: The query enters a "State Graph" (Retrieve -> Analyze -> Synthesize).
3. **Temporal Search**: We search the database but can also filter by session numbers.
4. **Contradiction Detection**: If multiple sessions discuss the topic, we check if the professor's explanation changed over time.
5. **Synthesis**: A "Teaching Assistant" LLM prompt writes the final answer based ONLY on the retrieved facts.

---

## 🛠️ The Core Components

### 1. The "Temporal" Brain (`retrieval/retriever.py`)
Standard search just finds "similar" text. Ours is smarter:
- **The Secret Sauce**: Every chunk has a `session_number`.
- **Why it matters**: It allows you to track **Concept Evolution**. You can see how a professor introduced a topic in Week 1 and made it more complex in Week 10.

### 2. The Agentic Workflow (`retrieval/graph.py`)
We use **LangGraph** to manage logic. It’s modular:
- **`retrieve_node`**: Fetches facts.
- **`analyze_node`**: Checks for contradictions.
- **`synthesize_node`**: Writes the final answer.

### 3. Professional Standards
- **`config.py`**: Centralizes all settings (models, API keys, paths). No more hardcoded strings.
- **`logger.py`**: Uses Python's `logging` module to track system behavior, making it "production-ready."

---

## 💡 Interview Talking Points (The "Human" Edge)

If an interviewer asks: *"What was the hardest part?"* or *"Why is this special?"*

1.  **Temporal Consistency**: "Standard RAG ignores time. I built a system that recognizes that lectures are a sequence, allowing us to find when a professor contradicts their own earlier statements."
2.  **Hardware Optimization**: "I didn't just use an API. I optimized local transcription using Mac GPU acceleration (MPS), which drastically reduced ingestion time."
3.  **Defensive Coding**: "I handled messy real-world data, like silent gaps in YouTube audio and API rate limits, by implementing robust logging and fallback topics."

---

## 📂 File Map
- `ingest.py`: Entry point for adding data.
- `ui/app.py`: The Premium Streamlit dashboard.
- `models.py`: Defines the "Shape" of our data.
- `retrieval/contradiction.py`: The logic for "Did the professor change their mind?"
