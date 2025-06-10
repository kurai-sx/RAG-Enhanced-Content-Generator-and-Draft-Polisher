# 📝 Campaign Draft Generator + Polisher (RAG + ChromaDB + OpenAI)

This is a Streamlit-based tool that allows content creators to either:
- 🪄 **Generate** a full campaign story from a simple idea and category, or
- 📝 **Polish** an existing draft using SOP guidelines, past campaigns, and banned keyword filters.

It uses:
- **OpenAI GPT-4** for generation + refinement
- **ChromaDB** for storing and retrieving past content contextually
- **LangChain** for chunking and embedding logic

---

## 🎯 Use Cases

- Crowdfunding platforms like Donatekart, Milaap, Ketto
- NGOs creating stories across categories like Medical, Hunger, Elderly, Animals, Education
- Freelancers or content teams streamlining campaign creation

---

## ✨ Features

- 🪄 **Generate from Idea**: Create new stories from a category + objective
- 🧠 **RAG-Based Polishing**: Retrieve examples and SOPs based on category and refine the draft accordingly
- ❌ **Banned Keyword Filtering**: Enforces content compliance using rule-based PDF
- 🔄 **Self-Learning**: Saves polished outputs to ChromaDB for better future retrieval
- 💬 Built using **Streamlit** UI

---

## 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/campaign-draft-tool.git
cd campaign-draft-tool
pip install -r requirements.txt
```
## ⚙️ Usage
```bash
streamlit run app.py
```

## 📃 License
Suraj's License – free to use and modify.
