# 🎓 Lecture Memory

**Lecture Memory** is an advanced RAG (Retrieval-Augmented Generation) system designed for students to manage high-volume video lectures. It doesn't just search; it tracks how concepts evolve over a semester and detects when a professor contradicts a previous lecture.

---

## 🚀 Key Features

- **🎬 Source Ingestion**: Direct YouTube ingestion with auto-cleanup of local assets.
- **🎙️ Fast Transcription**: Transcription of lectures using `OpenAI Whisper`.
- **🤖 Agentic Workflow**: Used **LangGraph** for modular retrieval and synthesis.
- **🧠 Temporal RAG**: Retrieval that understands chronological sequence.
- **⚠️ Contradiction Detection**: Cross-references early lectures with later ones to find conflicting claims or evolved definitions.
- **⏳ Concept Timeline**: Visualizes how a single topic was introduced, expanded, and summarized across the entire course.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Vector DB**: Qdrant (Local Docker)
- **Transcription**: OpenAI Whisper (`tiny` model for speed)
- **Embeddings**: `sentence-transformers` (all-MiniLM-L6-v2)
- **LLM**: GPT-4o-mini (via GitHub Models API)

---

## 💡 Engineering Challenges I Solved

### 1. The "Temporal Context" Problem
Most RAG systems just find the most similar text. But in a course, a definition in Week 1 might be simplified, while Week 10 is the "correct" complex version. I implemented a **Temporal Retriever** that maps chunks to session numbers, allowing the LLM to prioritize or compare explanations chronologically.

### 2. GPU Acceleration on Apple Silicon
Local transcription was originally too slow. I refactored the pipeline to use PyTorch's `mps` device, enabling hardware acceleration on my Mac's M-series chip, reducing transcription time by ~70%.



---

## 🚦 Getting Started

1. **Start Qdrant**:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

2. **Check System**:
   ```bash
   python main.py
   ```

3. **Launch the UI**:
   ```bash
   uv run streamlit run ui/app.py
   ```

3. **Ingest your first lecture**:
   Go to the **"Add Lecture"** tab in the UI and paste a YouTube URL!
