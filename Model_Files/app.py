# app.py

import streamlit as st
import os
import logging
from utils.load_txt import load_txt_files
from utils.load_pdf import load_banned_keywords_pdf
from utils.load_csv import load_successful_campaigns
from chunk_and_embed import chunk_documents, embed_chunks
from ingest_to_chroma import upsert_to_chroma
from polish_draft import polish_campaign_draft
from config import CHROMA_DIR

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

logger.info("Initializing Campaign Draft Polisher application")

st.set_page_config(
    page_title="✨ Campaign Draft Polisher",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    "<h1 style='text-align: center; color: #FFFFFF;'>📝 Campaign Draft Polisher</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>RAG + ChromaDB powered content refinement system for fundraising campaigns</p>",
    unsafe_allow_html=True
)


# Place selectors side by side
sel_col1, sel_col2 = st.columns(2)
with sel_col1:
    st.subheader("📂 Select Campaign Category")
    try:
        with open(os.path.join(BASE_DIR, "Data", "campaign_categories.txt"), 'r') as f:
            categories = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        categories = ["General"]
    category = st.selectbox("Choose Category", categories)
with sel_col2:
    st.subheader("Select Action")
    action = st.radio("What do you want to do?", ["Polish Draft", "Generate Draft"], horizontal=True)

# Show relevant input fields for each action
if action == "Generate Draft":
    st.subheader("🛠️ Draft Generation Settings")
    objective = st.text_area("What is the main objective of your campaign?", height=100)
    tone = st.selectbox("Choose tone", ["emotional", "factual", "urgent", "inspirational"], index=0)
else:
    st.subheader("✍️ Paste Raw Campaign Draft")
    user_draft = st.text_area("Enter the raw draft:", height=300)

# --- Action Button: Always above the output ---
action_btn_label = "🚀 Generate Draft" if action == "Generate Draft" else "✨ Polish Draft"
action_btn_clicked = st.button(action_btn_label, key="action_btn")

# --- Action Logic ---
if action_btn_clicked:
    if action == "Generate Draft":
        logger.info(f"Generating new draft for category '{category}' with objective '{objective}' and tone '{tone}'")
        if not objective.strip():
            st.warning("Please provide an objective for the campaign.")
            logger.warning("No objective provided for draft generation")
        else:
            with st.spinner("Generating campaign draft..."):
                try:
                    from generate_draft import generate_campaign
                    generated_draft = generate_campaign(category, objective, tone)
                    st.session_state["output"] = generated_draft
                    logger.info("Draft generated successfully and stored in session state")
                except Exception as e:
                    logger.error(f"Error generating draft: {str(e)}")
                    st.error(f"Error generating draft: {str(e)}")
    else:
        logger.info("Starting draft polishing process")
        with st.spinner("Loading knowledge base..."):
            logger.info("Loading SOP documents")
            sop_chunks = load_txt_files(os.path.join(BASE_DIR, "Data", "Rules_SOP"))
            logger.info(f"Loaded {len(sop_chunks)} SOP chunks")

            logger.info("Loading successful campaigns")
            campaign_chunks = load_successful_campaigns(os.path.join(BASE_DIR, "Data", "Succcessful_Campaings.csv"))
            logger.info(f"Loaded {len(campaign_chunks)} campaign chunks")

            logger.info("Loading banned keywords")
            banned_text = load_banned_keywords_pdf(os.path.join(BASE_DIR, "Data", "banned_keywords.pdf"))
            logger.info(f"Loaded banned keywords document")

            all_docs = sop_chunks + campaign_chunks
            logger.info(f"Total documents to process: {len(all_docs)}")

            logger.info("Chunking documents")
            chunks = chunk_documents(all_docs)
            logger.info(f"Created {len(chunks)} chunks")

            logger.info("Embedding chunks")
            vectors = embed_chunks(chunks)
            logger.info("Finished embedding chunks")

            logger.info("Upserting to ChromaDB")
            upsert_to_chroma(vectors, chunks)
            logger.info("Finished upserting to ChromaDB")

        with st.spinner("Refining your draft..."):
            logger.info("Polishing campaign draft")
            try:
                polished_output = polish_campaign_draft(user_draft, banned_text, category)
                logger.info("Successfully polished draft")
            except Exception as e:
                logger.error(f"Error polishing draft: {str(e)}")
                raise

        st.session_state["output"] = polished_output
        logger.info("Polished output stored in session state")

# --- Display polished output below controls ---
st.subheader("✅ Polished Output")
if "output" in st.session_state:
    st.markdown(
        f"<div style='padding: 15px; border-radius: 10px; border-left: 6px solid #6C63FF;'>"
        f"{st.session_state['output'].replace(chr(10), '<br>')}</div>",
        unsafe_allow_html=True
    )
else:
    st.info("Polished output will appear here after you submit a draft.")
