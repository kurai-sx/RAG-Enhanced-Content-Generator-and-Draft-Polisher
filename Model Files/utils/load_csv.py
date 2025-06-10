# utils/load_csv.py

import pandas as pd

def load_successful_campaigns(csv_path):
    df = pd.read_csv(csv_path)
    records = []
    for _, row in df.iterrows():
        content = " ".join([str(cell) for cell in row if pd.notnull(cell)])
        records.append({
            "source": "successful_campaigns",
            "content": content
        })
    return records
