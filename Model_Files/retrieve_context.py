# retrieve_context.py

import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from config import OPENAI_API_KEY, CHROMA_DIR, EMBED_MODEL

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name="campaign_knowledge")

def retrieve_context(query: str, category: str, top_k: int = 5):

    embedder = OpenAIEmbeddings(model=EMBED_MODEL, openai_api_key=OPENAI_API_KEY)
    query_vector = embedder.embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where={"category": category}
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    
    context_chunks = [f"{meta.get('source', 'unknown')}\n{doc}" for doc, meta in zip(documents, metadatas)]
    return "\n---\n".join(context_chunks)
