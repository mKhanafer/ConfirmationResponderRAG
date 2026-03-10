"""
Configuration settings for Confirmation AI
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Groq API Settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Embedding Settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ChromaDB Settings
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "confirmation_docs"

# Text Splitting Settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200
TEXT_SPLITTER_SEPARATORS = ["\n## ", "\n### ", "\n\n", "\n", " "]

# RAG Settings
TOP_K = 5
SIMILARITY_THRESHOLD = 0.3
MAX_HISTORY_TURNS = 10

# Session Settings
SESSION_TIMEOUT_MINUTES = 60

# Docs Directory
DOCS_DIR = "./docs"
