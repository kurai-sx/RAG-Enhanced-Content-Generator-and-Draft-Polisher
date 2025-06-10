# ingest_to_chroma.py

import chromadb
from config import CHROMA_DIR

def upsert_to_chroma(vectors, chunks):
    """
    Store document chunks and embeddings in Chroma vector database
    """
    # Initialize Chroma client with new API
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    
    # Get or create collection
    collection = chroma_client.get_or_create_collection(name="campaign_knowledge")
    
    # Prepare documents and IDs
    documents = [chunk["content"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [f"doc_{i}" for i in range(len(documents))]
    
    # Upsert to Chroma
    collection.upsert(
        ids=ids,
        embeddings=vectors,
        metadatas=metadatas,
        documents=documents
    )
    
    print(f"✅ {len(ids)} documents upserted to Chroma")
