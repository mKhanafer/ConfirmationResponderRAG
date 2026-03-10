"""
FastAPI application for Confirmation AI
Provides REST API endpoints with SSE streaming support
"""
import json
import asyncio
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from .rag import get_assistant
from .ingest import main as run_ingestion


# Pydantic models for request/response
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: list


class HealthResponse(BaseModel):
    status: str
    message: str


# Initialize FastAPI app
app = FastAPI(
    title="Confirmation AI API",
    description="AI-powered RAG Chatbot for Thomson Reuters Confirmation Migration & User Guides",
    version="1.0.0"
)

# Enable CORS for all origins (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Initialize assistant on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the RAG assistant on startup"""
    print("🚀 Starting Confirmation AI API...")
    try:
        get_assistant()
        print("✅ RAG Assistant initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize RAG Assistant: {e}")
        print("   Make sure you have run 'python app/ingest.py' first to create the vector store")


@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint - redirect to docs or health check"""
    return {
        "message": "Confirmation AI API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "chat_stream": "/chat/stream",
            "ingest": "/ingest",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        assistant = get_assistant()
        # Verify vectorstore is accessible
        collection_count = assistant.vectorstore._collection.count()
        
        return HealthResponse(
            status="healthy",
            message=f"API is running. Vector store contains {collection_count} documents."
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Standard chat endpoint (non-streaming)
    
    Request body:
    {
        "session_id": "unique-session-id",
        "message": "How do I migrate from CurrentGen to NextGen?"
    }
    
    Response:
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
    """
    try:
        assistant = get_assistant()
        result = assistant.chat(request.session_id, request.message)
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint using Server-Sent Events (SSE)
    
    Request body: Same as /chat
    
    Response: SSE stream with events:
    - data: {"type": "response", "content": "chunk of text"}
    - data: {"type": "sources", "content": [...]}
    """
    
    async def event_generator():
        try:
            assistant = get_assistant()
            
            # Stream the response
            for chunk in assistant.chat_stream(request.session_id, request.message):
                # Format as SSE
                data = json.dumps(chunk)
                yield f"data: {data}\n\n"
                
                # Small delay to prevent overwhelming the client
                await asyncio.sleep(0.01)
            
            # Send done signal
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
        except Exception as e:
            error_data = json.dumps({
                "type": "error",
                "content": f"Error: {str(e)}"
            })
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/ingest")
async def trigger_ingestion():
    """
    Trigger document re-ingestion
    
    This will reload all markdown files from the docs/ directory,
    split them into chunks, and rebuild the vector store.
    
    Use this endpoint when you've updated the documentation files.
    """
    try:
        # Run ingestion in background (this may take a while)
        # In production, you'd want to use a task queue like Celery
        run_ingestion()
        
        return {
            "status": "success",
            "message": "Documents ingested successfully. Vector store updated."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during ingestion: {str(e)}"
        )


@app.get("/sessions/{session_id}")
async def get_session_info(session_id: str):
    """
    Get information about a specific session
    """
    try:
        assistant = get_assistant()
        session = assistant.session_manager.get_session(session_id)
        
        return {
            "session_id": session_id,
            "message_count": len(session["history"]),
            "last_activity": session["last_activity"].isoformat(),
            "history": session["history"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving session: {str(e)}"
        )


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """
    Clear a specific session's history
    """
    try:
        assistant = get_assistant()
        if session_id in assistant.session_manager.sessions:
            del assistant.session_manager.sessions[session_id]
            return {
                "status": "success",
                "message": f"Session {session_id} cleared"
            }
        else:
            return {
                "status": "not_found",
                "message": f"Session {session_id} not found"
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing session: {str(e)}"
        )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc)
        }
    )


if __name__ == "__main__":
    # Run with: python app/main.py
    # Or better: uvicorn app.main:app --reload
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
