# chunk_and_embed.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from config import EMBED_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, OPENAI_API_KEY


def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "]
    )
    all_chunks = []
    for doc in docs:
        splits = splitter.split_text(doc["content"])
        for chunk in splits:
            all_chunks.append({
                "content": chunk,
                "metadata": {"source": doc["source"]}
            })
    return all_chunks


def embed_chunks(chunks):
    embedder = OpenAIEmbeddings(model=EMBED_MODEL, openai_api_key=OPENAI_API_KEY)
    texts = [chunk["content"] for chunk in chunks]
    return embedder.embed_documents(texts)
