# VidQuery-RAG

Chat with YouTube videos using RAG and LLMs. Extract information, ask questions, and get answers directly from video content.

## Overview

VidQuery-RAG is a full-stack application that lets you have a conversation with any YouTube video. Instead of scrubbing through timestamps, you can ask questions and get relevant answers pulled directly from the video's transcript.

The project started as a Google Colab experiment for understanding RAG pipelines and evolved into a proper web application with a FastAPI backend and a simple HTML/CSS/JavaScript frontend.

## Features

- **YouTube Integration** – Drop a video URL and start asking questions
- **RAG Pipeline** – Retrieves relevant transcript segments and generates contextual answers
- **Real-time Processing** – Handles video transcription and vectorization efficiently
- **Conversational UI** – Simple, no-frills chat interface
- **API-driven** – Clean separation between backend (FastAPI) and frontend (HTML/JS)

## Tech Stack

**Backend:**
- Python
- FastAPI
- LangChain
- FAISS (vector database)
- OpenRouter (LLM access)

**Frontend:**
- HTML/CSS/JavaScript (single-file interface, AI-assisted with manual iteration)

## Project Structure

```
VidQuery-RAG/
├── backend/              # FastAPI application + RAG pipeline
│   ├── app.py           # Main FastAPI server
│   ├── rag_pipeline.py  # RAG logic and LLM integration
│   ├── utils.py         # Helper functions
│   └── requirements.txt  # Python dependencies
├── frontend/            # Static frontend files
│   ├── index.html       # Single-page chat interface
│   └── style.css        # Styling
├── notebooks/           # Jupyter notebooks (experimentation)
│   └── exploration.ipynb
└── README.md
```

## Local Setup

### Prerequisites
- Python 3.10+
- pip or uv
- An OpenRouter API key (free tier available)
- YouTube video links (transcripts must be available)

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/rohitnath-dev/VidQuery-RAG.git
   cd VidQuery-RAG
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export OPENROUTER_API_KEY="your_api_key_here"
   ```

4. **Run the backend**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:8000`

5. **Open the frontend**
   Simply open `frontend/index.html` in your browser (or serve it with a simple HTTP server):
   ```bash
   cd ../frontend
   python -m http.server 8080
   ```
   Then navigate to `http://localhost:8080`

## API Endpoints

- `POST /api/chat` – Send a message and get a response
  - Body: `{ "video_url": "...", "message": "..." }`
  - Returns: `{ "response": "...", "sources": [...] }`

- `POST /api/load-video` – Load and process a YouTube video
  - Body: `{ "video_url": "..." }`
  - Returns: `{ "status": "loaded", "chunks": N }`

## Deployment Notes

The backend can be deployed to any platform that supports Python/FastAPI (Heroku, Railway, Render, etc.). For production:

- Use environment variables for API keys
- Enable CORS appropriately
- Consider caching FAISS vectors for repeated queries
- Add rate limiting to prevent abuse

The frontend is static and can be deployed to any CDN or static host (Vercel, GitHub Pages, etc.).

## Current Limitations

- YouTube videos without auto-generated or manual transcripts won't work
- Long videos (2+ hours) may require chunking optimizations
- No persistent conversation history (resets per session)
- FAISS vectors are stored in memory (rebuilds on restart)
- No user authentication or multi-user support
- Response quality depends on video transcript quality and LLM availability

## Future Improvements

- Persistent vector storage (PostgreSQL with pgvector)
- Conversation history and bookmarking
- Support for other video platforms (Vimeo, etc.)
- Local LLM option for privacy
- Better chunk overlapping and retrieval strategies
- User accounts and query analytics
- Improved UI/UX for mobile devices

## Development Notes

**Frontend:** The UI was generated and iterated with AI tools, then manually refined. It's functional and minimal – not designed to be fancy.

**Backend:** The RAG pipeline, FastAPI integration, and LLM orchestration were implemented manually from scratch. If you want to understand how it works, check out `backend/rag_pipeline.py`.

**Notebooks:** Early experimentation happened in Jupyter notebooks (saved in `notebooks/`). They're kept for reference if you want to see how the idea evolved.

## Acknowledgements

- LangChain for the RAG framework
- OpenRouter for LLM access
- YouTube's transcript API
- FAISS for efficient vector search
- Everyone who gave feedback during early testing

---

Built by [rohitnath-dev](https://github.com/rohitnath-dev). Questions? Open an issue or feel free to reach out.
