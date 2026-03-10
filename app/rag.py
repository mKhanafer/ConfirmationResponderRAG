"""
RAG chain logic for Confirmation AI
Handles retrieval, generation, session management, and special behaviors
"""
import re
import warnings
import urllib3
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Suppress SSL warnings in corporate environments
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from .config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    EMBEDDING_MODEL,
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME,
    TOP_K,
    SIMILARITY_THRESHOLD,
    MAX_HISTORY_TURNS,
    SESSION_TIMEOUT_MINUTES
)
from .prompts import SYSTEM_PROMPT, PII_WARNING, OUT_OF_SCOPE_MESSAGE


class SessionManager:
    """Manages conversation sessions with history and timeout"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def get_session(self, session_id: str) -> Dict:
        """Get or create a session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "history": [],
                "last_activity": datetime.now()
            }
        else:
            # Update last activity
            self.sessions[session_id]["last_activity"] = datetime.now()
        
        # Clean expired sessions
        self._cleanup_expired_sessions()
        
        return self.sessions[session_id]
    
    def add_to_history(self, session_id: str, user_message: str, ai_response: str):
        """Add a conversation turn to session history"""
        session = self.get_session(session_id)
        session["history"].append({
            "user": user_message,
            "ai": ai_response,
            "timestamp": datetime.now()
        })
        
        # Limit history to MAX_HISTORY_TURNS
        if len(session["history"]) > MAX_HISTORY_TURNS:
            session["history"] = session["history"][-MAX_HISTORY_TURNS:]
    
    def get_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        session = self.get_session(session_id)
        return session["history"]
    
    def _cleanup_expired_sessions(self):
        """Remove sessions that have been inactive for too long"""
        cutoff_time = datetime.now() - timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if session["last_activity"] < cutoff_time
        ]
        for sid in expired_sessions:
            del self.sessions[sid]


class RAGAssistant:
    """Main RAG assistant with retrieval and generation capabilities"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize embeddings, vectorstore, and LLM"""
        print("🔧 Initializing RAG components...")
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Load vectorstore
        self.vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIR
        )
        
        # Initialize LLM with SSL verification disabled for corporate networks
        import httpx
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        http_client = httpx.Client(verify=False, timeout=60.0)
        
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL,
            temperature=0.1,
            max_tokens=2000,
            http_client=http_client
        )
        
        print("✅ RAG components initialized")
    
    def detect_pii(self, message: str) -> bool:
        """
        Detect if message contains PII or sensitive information
        Returns True if PII detected
        """
        # Patterns for API keys, tokens, passwords
        patterns = [
            r'api[_-]?key[:\s=]+[\w\-]{20,}',  # API keys
            r'token[:\s=]+[\w\-]{20,}',  # Tokens
            r'password[:\s=]+\S+',  # Passwords
            r'secret[:\s=]+\S+',  # Secrets
            r'bearer\s+[\w\-\.]+',  # Bearer tokens
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\s*[:\s]+\S+',  # Email with credentials
        ]
        
        message_lower = message.lower()
        for pattern in patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False
    
    def retrieve_context(self, query: str) -> Tuple[List[str], List[Dict], bool]:
        """
        Retrieve relevant chunks from vectorstore
        Returns: (context_texts, sources, is_ambiguous)
        """
        # Perform similarity search with scores
        results = self.vectorstore.similarity_search_with_score(query, k=TOP_K)
        
        # Filter by similarity threshold
        filtered_results = [
            (doc, score) for doc, score in results
            if score >= SIMILARITY_THRESHOLD
        ]
        
        if not filtered_results:
            return [], [], False
        
        # Extract context and sources
        context_texts = []
        sources = []
        source_files = set()
        
        for doc, score in filtered_results:
            context_texts.append(doc.page_content)
            source_info = {
                "source": doc.metadata.get("source", "Unknown"),
                "section": doc.metadata.get("section", "Unknown"),
                "relevance": float(score)
            }
            sources.append(source_info)
            source_files.add(doc.metadata.get("source", "Unknown"))
        
        # Check for ambiguity (multiple source files with similar relevance)
        is_ambiguous = self._check_ambiguity(filtered_results, source_files)
        
        return context_texts, sources, is_ambiguous
    
    def _check_ambiguity(self, results: List[Tuple], source_files: set) -> bool:
        """
        Check if query is ambiguous based on retrieved sources
        Ambiguity occurs when multiple different source files have similar top scores
        """
        if len(source_files) <= 1:
            return False
        
        # Get source file scores
        source_scores = {}
        for doc, score in results:
            source = doc.metadata.get("source", "Unknown")
            if source not in source_scores:
                source_scores[source] = []
            source_scores[source].append(score)
        
        # Get max score for each source
        source_max_scores = {src: max(scores) for src, scores in source_scores.items()}
        
        # Check if we have both Responder and Requester docs with similar scores
        responder_docs = [src for src in source_files if "responder" in src.lower()]
        requester_docs = [src for src in source_files if "requester" in src.lower()]
        
        if responder_docs and requester_docs:
            responder_max = max(source_max_scores.get(src, 0) for src in responder_docs)
            requester_max = max(source_max_scores.get(src, 0) for src in requester_docs)
            
            # If both have high scores (within 0.1), it's ambiguous
            if abs(responder_max - requester_max) < 0.1 and min(responder_max, requester_max) > 0.4:
                return True
        
        return False
    
    def format_chat_history(self, session_id: str) -> str:
        """Format chat history for prompt"""
        history = self.session_manager.get_history(session_id)
        
        if not history:
            return "No previous conversation."
        
        formatted = []
        for turn in history[-5:]:  # Last 5 turns only
            formatted.append(f"User: {turn['user']}")
            formatted.append(f"Assistant: {turn['ai']}")
        
        return "\n".join(formatted)
    
    def generate_response(
        self, 
        query: str, 
        context_texts: List[str], 
        session_id: str,
        is_ambiguous: bool = False
    ) -> str:
        """Generate response using LLM"""
        
        # Handle ambiguity first
        if is_ambiguous:
            return ("I found information that could apply to different areas. "
                   "Could you clarify:\n\n"
                   "• Are you asking about **Responder (Bank AutoProcess APIs)** or **Requester (Auditor submission)**?\n"
                   "• Are you working with **CurrentGen** or **NextGen**?\n\n"
                   "This will help me provide the most accurate information.")
        
        # Format context
        context = "\n\n---\n\n".join(context_texts) if context_texts else "No relevant context found."
        
        # Format chat history
        chat_history = self.format_chat_history(session_id)
        
        # Build prompt
        prompt = f"""{SYSTEM_PROMPT}

## Retrieved Documentation Context
{context}

## Conversation History
{chat_history}

## Current Question
{query}

Answer the question using ONLY the retrieved documentation above. If the answer is not in the context, say: "I don't have enough information to answer that. Please contact ConfirmationResponderAPI@thomsonreuters.com for further assistance."
"""
        
        # Generate response
        messages = [HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        
        return response.content
    
    def chat(self, session_id: str, user_message: str) -> Dict:
        """
        Main chat function that handles the full RAG pipeline
        Returns: {"response": str, "sources": List[Dict]}
        """
        # Check for PII first
        if self.detect_pii(user_message):
            return {
                "response": PII_WARNING,
                "sources": []
            }
        
        # Retrieve context
        context_texts, sources, is_ambiguous = self.retrieve_context(user_message)
        
        # If no relevant chunks found, return out-of-scope message
        if not context_texts and not is_ambiguous:
            response = OUT_OF_SCOPE_MESSAGE
            self.session_manager.add_to_history(session_id, user_message, response)
            return {
                "response": response,
                "sources": []
            }
        
        # Generate response
        response = self.generate_response(
            user_message, 
            context_texts, 
            session_id,
            is_ambiguous
        )
        
        # Add to history
        self.session_manager.add_to_history(session_id, user_message, response)
        
        # Deduplicate sources
        unique_sources = []
        seen = set()
        for source in sources:
            key = (source["source"], source["section"])
            if key not in seen:
                seen.add(key)
                unique_sources.append(source)
        
        return {
            "response": response,
            "sources": unique_sources
        }
    
    def chat_stream(self, session_id: str, user_message: str):
        """
        Streaming version of chat function
        Yields chunks of the response
        """
        # Check for PII first
        if self.detect_pii(user_message):
            yield {"type": "response", "content": PII_WARNING}
            yield {"type": "sources", "content": []}
            return
        
        # Retrieve context
        context_texts, sources, is_ambiguous = self.retrieve_context(user_message)
        
        # If no relevant chunks found
        if not context_texts and not is_ambiguous:
            response = OUT_OF_SCOPE_MESSAGE
            self.session_manager.add_to_history(session_id, user_message, response)
            yield {"type": "response", "content": response}
            yield {"type": "sources", "content": []}
            return
        
        # Handle ambiguity
        if is_ambiguous:
            response = ("I found information that could apply to different areas. "
                       "Could you clarify:\n\n"
                       "• Are you asking about **Responder (Bank AutoProcess APIs)** or **Requester (Auditor submission)**?\n"
                       "• Are you working with **CurrentGen** or **NextGen**?\n\n"
                       "This will help me provide the most accurate information.")
            self.session_manager.add_to_history(session_id, user_message, response)
            yield {"type": "response", "content": response}
            yield {"type": "sources", "content": sources}
            return
        
        # Format context and history
        context = "\n\n---\n\n".join(context_texts)
        chat_history = self.format_chat_history(session_id)
        
        # Build prompt
        prompt = f"""{SYSTEM_PROMPT}

## Retrieved Documentation Context
{context}

## Conversation History
{chat_history}

## Current Question
{user_message}

Answer the question using ONLY the retrieved documentation above. If the answer is not in the context, say: "I don't have enough information to answer that. Please contact ConfirmationResponderAPI@thomsonreuters.com for further assistance."
"""
        
        # Stream response
        full_response = ""
        for chunk in self.llm.stream([HumanMessage(content=prompt)]):
            content = chunk.content
            full_response += content
            yield {"type": "response", "content": content}
        
        # Add to history
        self.session_manager.add_to_history(session_id, user_message, full_response)
        
        # Send sources
        unique_sources = []
        seen = set()
        for source in sources:
            key = (source["source"], source["section"])
            if key not in seen:
                seen.add(key)
                unique_sources.append(source)
        
        yield {"type": "sources", "content": unique_sources}


# Global instance
_assistant = None

def get_assistant() -> RAGAssistant:
    """Get or create the global RAG assistant instance"""
    global _assistant
    if _assistant is None:
        _assistant = RAGAssistant()
    return _assistant
