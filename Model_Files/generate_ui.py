# generate_ui.py

import streamlit as st
from generate_draft import generate_campaign

def show_generate_ui(category, categories):
    st.subheader("🎯 Describe Your Campaign Objective")
    objective = st.text_area("e.g., Rescue 40 injured animals from highway accidents", height=200)
    tone = st.selectbox("Choose Tone", ["emotional", "factual", "hopeful", "urgent"])

    if st.button("🚀 Generate Draft"):
        with st.spinner("Generating campaign story..."):
            generated_output = generate_campaign(category, objective, tone)
        st.subheader("✅ Generated Campaign Draft")
        st.text_area("Output", generated_output, height=300)
