import os
from utils.load_txt import load_txt_files
from utils.load_csv import load_successful_campaigns
from chunk_and_embed import chunk_documents, embed_chunks
from ingest_to_chroma import upsert_to_chroma

# Always resolve paths relative to the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sop_chunks = load_txt_files(os.path.join(BASE_DIR, "Data", "Rules_SOP"))
campaign_chunks = load_successful_campaigns(os.path.join(BASE_DIR, "Data", "Succcessful_Campaings.csv"))

all_docs = sop_chunks + campaign_chunks

# Chunk & embed once
chunks = chunk_documents(all_docs)
vectors = embed_chunks(chunks)

# Upsert to ChromaDB once
upsert_to_chroma(vectors, chunks)

print("✅ Embedding completed and stored in ChromaDB.")