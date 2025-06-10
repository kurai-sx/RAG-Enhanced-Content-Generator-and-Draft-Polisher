# utils/load_txt.py

import os

def load_txt_files(folder_path):
    txt_chunks = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                text = f.read()
                txt_chunks.append({
                    "source": filename,
                    "content": text
                })
    return txt_chunks
