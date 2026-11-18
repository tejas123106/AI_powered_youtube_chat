# YouTube AI Assistant 🎥🤖

An AI-powered Chrome Extension that allows users to interact with YouTube videos using natural language. Ask questions, generate summaries, and retrieve relevant information directly from video transcripts using Retrieval-Augmented Generation (RAG).

## 🚀 Features

- **YouTube Transcript Extraction:** Automatically retrieves available video transcripts.
- **Multilingual Transcript Support:** Supports English and Hindi transcript retrieval when available.
- **AI-Powered Question Answering:** Ask questions about video content and receive context-aware responses.
- **Video Summarization:** Generate summaries from complete video transcripts.
- **Semantic Search:** Uses multilingual Sentence Transformers and FAISS to retrieve relevant transcript chunks.
- **Timestamp References:** Provides relevant timestamps to help users navigate to specific video sections.
- **Local LLM Integration:** Uses Ollama with Qwen 2.5 (3B) for AI-generated responses.

## 🏗️ System Architecture

1. User opens a YouTube video and launches the Chrome Extension.
2. The extension extracts the YouTube video ID.
3. FastAPI receives the request and retrieves the available transcript.
4. Transcript text is divided into smaller chunks.
5. Sentence Transformers generates multilingual embeddings.
6. FAISS stores and retrieves relevant transcript chunks.
7. Ollama with Qwen 2.5 (3B) generates answers and summaries.
8. The extension displays the response with relevant timestamps.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python, JavaScript |
| Backend | FastAPI |
| AI Model | Qwen 2.5 (3B) |
| LLM Runtime | Ollama |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| Transcript Extraction | YouTube Transcript API |
| Frontend | HTML, CSS, JavaScript |
| Platform | Chrome Extension (Manifest V3) |

## 📂 Project Structure

```text
YouTube-AI-Assistant/
│
├── backend/
│   ├── main.py
│   ├── transcript.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── prompt.py
│   ├── llm.py
│   ├── rag.py
│   ├── summarize.py
│   └── requirements.txt
│
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   └── content.js
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YouTube-AI-Assistant
```

### 2. Set Up Python Environment

```bash
cd backend

python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama:

https://ollama.com/

Pull the Qwen model:

```bash
ollama pull qwen2.5:3b
```

Ensure Ollama is running before starting the backend.

### 5. Start FastAPI Backend

From the backend directory, run:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Install Chrome Extension

1. Open Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable Developer Mode.
4. Click **Load unpacked**.
5. Select the project's `extension` folder.
6. Open a YouTube video.
7. Click the YouTube AI Assistant extension icon.

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check backend status |
| POST | `/ingest` | Extract and process video transcripts |
| POST | `/ask` | Ask questions about video content |
| POST | `/summarize` | Generate video summaries |

## 🧠 RAG Workflow

The project uses Retrieval-Augmented Generation (RAG) to improve answer relevance.

- **Ingestion:** Extracts and chunks YouTube transcripts.
- **Embedding:** Converts transcript chunks into numerical vectors.
- **Indexing:** Stores embeddings in FAISS.
- **Retrieval:** Finds relevant chunks based on user questions.
- **Generation:** Uses Qwen 2.5 (3B) through Ollama to generate context-aware answers.

## 🔮 Future Enhancements

- Support for additional languages and translated transcripts.
- Streaming responses for faster user interaction.
- Improved timestamp accuracy and retrieval optimization.
- Public backend deployment and Chrome Web Store publication.
- User-selectable response languages.
- Enhanced conversational memory.
