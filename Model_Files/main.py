from utils.load_txt import load_txt_files
from utils.load_pdf import load_banned_keywords_pdf
from utils.load_csv import load_successful_campaigns
from chunk_and_embed import chunk_documents, embed_chunks
from ingest_to_chroma import upsert_to_chroma
from retrieve_context import retrieve_context
from polish_draft import polish_campaign_draft

# STEP 1: Load all knowledge base sources
sop_chunks = load_txt_files("./Rule_SOP")
campaign_chunks = load_successful_campaigns("./Successful_Campaings.csv")
banned_text = load_banned_keywords_pdf("./banned_keywords.pdf")

# STEP 2: Chunk and embed all content
all_docs = sop_chunks + campaign_chunks
chunks = chunk_documents(all_docs)
vectors = embed_chunks(chunks)

# STEP 3: Ingest into Chroma
upsert_to_chroma(vectors, chunks)

# STEP 4: Run the RAG-powered polish flow
sample_draft = """
This campaign supports a poor blind girl suffering from cancer. Her father can't afford the surgery. Please help.
"""

polished = polish_campaign_draft(sample_draft, banned_text, category="Medical")
print("\n--- Polished Draft ---\n")
print(polished)
