# polish_draft.py

from banned_keywords import extract_replacements, apply_replacements
from retrieve_context import retrieve_context
from config import OPENAI_API_KEY
from openai import OpenAI
from ingest_to_chroma import upsert_to_chroma
from chunk_and_embed import chunk_documents, embed_chunks
openai = OpenAI(api_key=OPENAI_API_KEY)


def polish_campaign_draft(draft: str, banned_text: str, category: str):
    context = retrieve_context(draft, category)
    banned_rules = extract_replacements(banned_text)
    cleaned_draft = apply_replacements(draft, banned_rules)

    system_prompt = (
    "You are a professional content editor for a crowdfunding platform. "
    "Based on the category context, examples, and SOPs, your job is to correct and polish the campaign draft. "
    "Ensure the story fits the emotional tone and structure suitable for the selected campaign category."
    )


    user_prompt = f"""
You are polishing a fundraising campaign draft.

### CONTEXT FROM SOPs AND PAST CAMPAIGNS (category: {category}):
{context}

### RAW DRAFT (with banned terms already cleaned):
{cleaned_draft}

### INSTRUCTIONS:
Polish the above draft into a final compelling campaign story. 
- Ensure the tone, urgency, and emotional appeal match the **'{category}'** category.
- Align language with successful campaigns in this domain.
- Ensure clarity, correctness, and engagement.

Only output the final polished version.
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    polished_output = response.choices[0].message.content.strip()
    new_chunk = {"content": polished_output, "metadata": {"source": "user_draft", "category": category}}
    new_chunks = [new_chunk]
    new_embeddings = embed_chunks(new_chunks)
    upsert_to_chroma(new_embeddings, new_chunks)  
    return polished_output
