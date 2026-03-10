"""
Document ingestion script for Confirmation AI
Loads markdown files, splits them into chunks, embeds them, and stores in ChromaDB
"""
import os
import re
from pathlib import Path
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from .config import (
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TEXT_SPLITTER_SEPARATORS,
    EMBEDDING_MODEL,
    DOCS_DIR
)


def extract_section_from_content(content: str, chunk_start: int) -> str:
    """
    Extract the section heading (## or ###) that precedes the chunk
    """
    # Get content up to chunk start
    preceding_content = content[:chunk_start]
    
    # Find the last ## or ### heading
    headings = re.findall(r'^#{2,3}\s+(.+)$', preceding_content, re.MULTILINE)
    
    if headings:
        return headings[-1].strip()
    return "Introduction"


def load_documents_from_directory(docs_dir: str) -> List[Document]:
    """
    Load all markdown files from the docs directory
    """
    docs_path = Path(docs_dir)
    documents = []
    
    if not docs_path.exists():
        print(f"⚠️  Warning: Documentation directory '{docs_dir}' does not exist.")
        print(f"   Creating directory and adding placeholder files...")
        docs_path.mkdir(parents=True, exist_ok=True)
        return documents
    
    md_files = list(docs_path.glob("*.md"))
    
    if not md_files:
        print(f"⚠️  Warning: No markdown files found in '{docs_dir}'")
        return documents
    
    print(f"\n📚 Loading documents from {docs_dir}...")
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                doc = Document(
                    page_content=content,
                    metadata={"source": md_file.name}
                )
                documents.append(doc)
                print(f"   ✓ Loaded {md_file.name} ({len(content)} chars)")
        except Exception as e:
            print(f"   ✗ Error loading {md_file.name}: {e}")
    
    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks with metadata
    """
    print(f"\n✂️  Splitting documents into chunks...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=TEXT_SPLITTER_SEPARATORS,
        length_function=len,
    )
    
    all_chunks = []
    
    for doc in documents:
        chunks = text_splitter.split_text(doc.page_content)
        
        for i, chunk in enumerate(chunks):
            # Find where this chunk appears in the original content
            chunk_start = doc.page_content.find(chunk)
            section = extract_section_from_content(doc.page_content, chunk_start)
            
            chunk_doc = Document(
                page_content=chunk,
                metadata={
                    "source": doc.metadata["source"],
                    "section": section,
                    "chunk_index": i
                }
            )
            all_chunks.append(chunk_doc)
        
        print(f"   ✓ {doc.metadata['source']}: {len(chunks)} chunks")
    
    print(f"\n   Total chunks created: {len(all_chunks)}")
    return all_chunks


def create_vector_store(chunks: List[Document]) -> Chroma:
    """
    Create or reset ChromaDB vector store and add documents
    """
    print(f"\n🔢 Creating embeddings using {EMBEDDING_MODEL}...")
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Clear existing collection if it exists
    print(f"   Initializing ChromaDB at {CHROMA_PERSIST_DIR}...")
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"   ✓ Cleared existing collection '{COLLECTION_NAME}'")
    except:
        print(f"   ℹ️  No existing collection to clear")
    
    # Create vector store
    print(f"   Creating new collection and embedding documents...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR
    )
    
    print(f"   ✓ Embedded and stored {len(chunks)} chunks")
    
    return vectorstore


def print_sample_chunks(vectorstore: Chroma, num_samples: int = 3):
    """
    Print sample chunks for verification
    """
    print(f"\n📋 Sample chunks from vector store:")
    print("=" * 80)
    
    # Get all documents
    collection = vectorstore._collection
    results = collection.peek(limit=num_samples)
    
    for i, (doc_id, document, metadata) in enumerate(zip(results['ids'], results['documents'], results['metadatas']), 1):
        print(f"\nChunk {i}:")
        print(f"  Source: {metadata.get('source', 'N/A')}")
        print(f"  Section: {metadata.get('section', 'N/A')}")
        print(f"  Content preview: {document[:200]}...")
        print("-" * 80)


def main():
    """
    Main ingestion pipeline
    """
    print("=" * 80)
    print("🚀 Starting Document Ingestion for Confirmation AI")
    print("=" * 80)
    
    # Load documents
    documents = load_documents_from_directory(DOCS_DIR)
    
    if not documents:
        print("\n⚠️  No documents to ingest. Please add markdown files to the docs/ directory.")
        return
    
    # Split documents
    chunks = split_documents(documents)
    
    if not chunks:
        print("\n⚠️  No chunks created. Check your documents.")
        return
    
    # Create vector store
    vectorstore = create_vector_store(chunks)
    
    # Print samples
    print_sample_chunks(vectorstore)
    
    print("\n" + "=" * 80)
    print("✅ Ingestion Complete!")
    print("=" * 80)
    print(f"   Total documents: {len(documents)}")
    print(f"   Total chunks: {len(chunks)}")
    print(f"   Persisted to: {CHROMA_PERSIST_DIR}")
    print(f"   Collection: {COLLECTION_NAME}")
    print("\n   Ready to start the API with: uvicorn app.main:app --reload")
    print("=" * 80)


if __name__ == "__main__":
    main()
