# banned_keywords.py

import re
from typing import List, Tuple

def extract_replacements(banned_text: str) -> List[Tuple[str, str]]:
    replacements = []
    for line in banned_text.splitlines():
        if "\t" in line:
            parts = line.split("\t")
            if len(parts) == 2:
                original, replacement = parts
                if original.strip() and replacement.strip():
                    replacements.append((original.strip(), replacement.strip()))
    return replacements

def apply_replacements(text: str, rules: List[Tuple[str, str]]) -> str:
    for banned, replacement in rules:
        pattern = re.compile(re.escape(banned), re.IGNORECASE)
        text = pattern.sub(replacement, text)
    return text
