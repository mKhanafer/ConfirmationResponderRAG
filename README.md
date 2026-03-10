# Confirmation AI

A free, self-hosted RAG (Retrieval-Augmented Generation) chatbot powered by AI that helps Thomson Reuters customers with:

- **Responder (Bank) API Migration**: Migrating AutoProcess APIs from CurrentGen to NextGen
- **Requester (Auditor) Workflows**: Submitting confirmation requests on CurrentGen and NextGen platforms

## 🚀 Tech Stack (All Free!)

- **LLM**: Groq API with Llama 3 70B (free tier)
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (local, free)
- **Vector Database**: ChromaDB (local, free)
- **Framework**: LangChain
- **API**: FastAPI with Server-Sent Events (SSE) streaming
- **Frontend**: Clean HTML/JS chat widget

## 📁 Project Structure

```
confirmation-assistant/
├── app/
│   ├── main.py              # FastAPI application
│   ├── rag.py               # RAG chain logic
│   ├── ingest.py            # Document ingestion
│   ├── config.py            # Configuration settings
│   └── prompts.py           # System prompts
├── docs/                    # Knowledge base (markdown files)
│   ├── responder_migration_guide.md
│   ├── requester_currentgen_guide.md
│   └── requester_nextgen_guide.md
├── static/
│   └── index.html           # Chat UI
├── chroma_db/               # Vector store (created after ingestion)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md
```

## ⚡ Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This will install all required packages. First-time installation may take 2-3 minutes.

### Step 2: Add Your Groq API Key

1. Get a free API key from [Groq Console](https://console.groq.com/keys)
2. Create a `.env` file in the project root:

```bash
# Windows
echo GROQ_API_KEY=your_api_key_here > .env

# Mac/Linux
echo "GROQ_API_KEY=your_api_key_here" > .env
```

Or manually create `.env` with:
```
GROQ_API_KEY=your_actual_api_key_here
```

### Step 3: Ingest Documents & Run

```bash
# Ingest documentation into vector store (one-time setup)
python app/ingest.py

# Start the API server
uvicorn app.main:app --reload
```

**That's it!** Open [http://localhost:8000/static/index.html](http://localhost:8000/static/index.html) in your browser.

## 📖 Detailed Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Internet connection (for downloading models and API calls)

### Installation Steps

1. **Clone or download this repository**

2. **Create a virtual environment (recommended)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI & Uvicorn (API server)
- LangChain (RAG framework)
- ChromaDB (vector database)
- Groq SDK (LLM)
- Sentence Transformers (embeddings)
- And other required packages

4. **Configure environment variables**

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: https://console.groq.com/keys

5. **Ingest your documents**

```bash
python app/ingest.py
```

This will:
- Load all `.md` files from `docs/` directory
- Split them into chunks (800 chars with 200 overlap)
- Create embeddings using HuggingFace model
- Store in ChromaDB at `./chroma_db/`
- Print sample chunks for verification

**Expected output:**
```
================================================================================
🚀 Starting Document Ingestion for Confirmation AI
================================================================================

📚 Loading documents from ./docs...
   ✓ Loaded responder_migration_guide.md (12547 chars)
   ✓ Loaded requester_currentgen_guide.md (15234 chars)
   ✓ Loaded requester_nextgen_guide.md (18932 chars)

✂️  Splitting documents into chunks...
   ✓ responder_migration_guide.md: 18 chunks
   ✓ requester_currentgen_guide.md: 22 chunks
   ✓ requester_nextgen_guide.md: 27 chunks

   Total chunks created: 67

🔢 Creating embeddings using all-MiniLM-L6-v2...
   ✓ Embedded and stored 67 chunks

📋 Sample chunks from vector store:
...
```

6. **Start the API server**

```bash
uvicorn app.main:app --reload
```

Server will start at: `http://localhost:8000`

7. **Open the chat interface**

Navigate to: [http://localhost:8000/static/index.html](http://localhost:8000/static/index.html)

## 🔧 Configuration

### Environment Variables (`.env`)

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Advanced Settings (`app/config.py`)

```python
# LLM Settings
GROQ_MODEL = "llama3-70b-8192"  # Groq model to use

# Embedding Settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # HuggingFace model

# ChromaDB Settings
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "confirmation_docs"

# Text Splitting
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200

# RAG Settings
TOP_K = 5  # Number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity score
MAX_HISTORY_TURNS = 10  # Conversation history limit

# Session Settings
SESSION_TIMEOUT_MINUTES = 60
```

## 📚 Adding Your Own Documentation

1. Add `.md` files to the `docs/` directory
2. Use Markdown formatting with clear headings:
   ```markdown
   # Main Title
   
   ## Section 1
   Content here...
   
   ## Section 2
   More content...
   ```
3. Re-run ingestion:
   ```bash
   python app/ingest.py
   ```

**Best practices for documentation:**
- Use clear section headings (`##` or `###`)
- Keep sections focused (400-1000 words each)
- Include code examples in fenced code blocks
- Use bullet points for lists
- Add clear keywords that users might search for

## 🌐 API Endpoints

### `POST /chat`
Standard chat endpoint (non-streaming)

**Request:**
```json
{
  "session_id": "unique-session-id",
  "message": "How do I migrate from CurrentGen to NextGen?"
}
```

**Response:**
```json
{
  "response": "To migrate from CurrentGen to NextGen...",
  "sources": [
    {
      "source": "responder_migration_guide.md",
      "section": "Migration Steps",
      "relevance": 0.89
    }
  ]
}
```

### `POST /chat/stream`
Streaming chat with Server-Sent Events (SSE)

Same request format, streams response chunks in real-time.

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running. Vector store contains 67 documents."
}
```

### `POST /ingest`
Trigger document re-ingestion (useful after updating docs)

### `GET /sessions/{session_id}`
Get session information and history

### `DELETE /sessions/{session_id}`
Clear a session's conversation history

## 🎯 Key Features

### 1. **Smart Disambiguation**
If your question could apply to multiple areas (Responder vs Requester, CurrentGen vs NextGen), the bot asks for clarification.

### 2. **PII Detection**
Automatically detects and blocks sensitive information (API keys, passwords, tokens) from being processed.

### 3. **Source Attribution**
Every response shows which documentation sections were used, with expandable source details.

### 4. **Session Management**
Maintains conversation context for up to 10 turns per session, with 1-hour timeout.

### 5. **Streaming Responses**
Real-time response streaming for better user experience.

### 6. **Out-of-Scope Handling**
If the question isn't related to Confirmation workflows, provides appropriate redirect message.

## 🧪 Testing

### Test the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "message": "What are the authentication changes in NextGen?"
  }'
```

### Test streaming:

```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "message": "How do I submit a confirmation request?"
  }'
```

## 🐛 Troubleshooting

### Issue: "No module named 'app'"

**Solution:** Run commands from the project root directory:
```bash
cd confirmation-assistant
python app/ingest.py
```

### Issue: "Groq API key not found"

**Solution:** Make sure `.env` file exists with valid API key:
```bash
# Check if .env exists
cat .env  # Mac/Linux
type .env  # Windows

# Should show:
GROQ_API_KEY=gsk_...
```

### Issue: "Collection not found" when starting API

**Solution:** Run ingestion first:
```bash
python app/ingest.py
```

### Issue: Slow response times

**Solutions:**
- Check your internet connection (Groq API requires internet)
- Reduce `TOP_K` in `config.py` (fewer chunks = faster)
- Use a smaller model (though Llama 3 70B is already optimized)

### Issue: "Port 8000 already in use"

**Solution:** Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

Then access at: `http://localhost:8001/static/index.html`

## 📊 Performance

- **Average Response Time**: 2-4 seconds (including retrieval and generation)
- **Embeddings**: Local, instant (no API calls)
- **Vector Search**: < 100ms for 1000+ chunks
- **Streaming**: Chunks delivered every ~50ms
- **Concurrent Users**: Supports multiple simultaneous sessions

## 🔒 Security Notes

- **Never commit `.env` file** - it contains your API key
- **PII Detection** is enabled by default
- **Session data** is stored in-memory only (cleared on restart)
- **CORS** is enabled for all origins by default - restrict for production:

```python
# In app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚀 Production Deployment

### Using Docker (recommended):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python app/ingest.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment variables for production:

```env
GROQ_API_KEY=your_production_key
GROQ_MODEL=llama3-70b-8192
LOG_LEVEL=info
```

### Scaling considerations:

- **Vector Store**: ChromaDB supports millions of documents
- **Sessions**: Consider Redis for distributed session storage
- **API Limits**: Groq free tier has rate limits - monitor usage
- **Load Balancing**: Use multiple API instances behind load balancer

## 📝 License

This project is provided as-is for Thomson Reuters internal use.

## 🤝 Support

For questions or issues:
- **Technical Issues**: Check troubleshooting section above
- **Groq API**: https://console.groq.com/docs
- **LangChain**: https://python.langchain.com/docs
- **ChromaDB**: https://docs.trychroma.com

## 🎓 Learn More

- [Groq Documentation](https://console.groq.com/docs)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [ChromaDB Guide](https://docs.trychroma.com/getting-started)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Built with ❤️ using free, open-source tools**

Happy chatting! 🤖
