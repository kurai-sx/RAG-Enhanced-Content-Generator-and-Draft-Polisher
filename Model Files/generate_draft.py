# generate_draft.py

from openai import OpenAI
from config import OPENAI_API_KEY

openai = OpenAI(api_key=OPENAI_API_KEY)

def generate_campaign(category: str, objective: str, tone: str = "emotional"):
    system_prompt = (
        "You are a campaign story writer for a crowdfunding platform. "
        "Based on successful campaigns and SOPs for the selected category, generate a compelling story."
    )
    user_prompt = f"""
Category: {category}
Objective: {objective}
Tone: {tone}

Write a complete, emotionally engaging campaign story that aligns with the selected category. Include:
- Background of the issue
- Who is affected and how
- Why funds are needed urgently
- A call to action for support
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()
