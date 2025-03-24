# jas/tokenizer.py
import re
from collections import Counter

def smart_tokenize(text):
    # Step 1: Tokenize everything including punctuation and whitespace
    base_tokens = re.findall(r"\s+|\w+(?:[’']\w+)?|[^\w\s]", text)

    # Step 2: Identify repeating special phrases like GOV.UK, factor.in, we.know etc.
    pattern = re.compile(r"\b(?:\w+[./?]\w+)+\b", re.IGNORECASE)
    candidates = pattern.findall(text)
    counted = Counter(candidates)
    repeated_phrases = [w for w, c in counted.items() if c > 1]

    # Step 3: Replace repeated phrases with markers
    specials = {phrase: f"§{i}§" for i, phrase in enumerate(repeated_phrases)}
    processed_text = text
    for phrase, marker in specials.items():
        processed_text = processed_text.replace(phrase, marker)

    # Step 4: Final tokenize again post-replacement
    final_tokens = re.findall(r"\s+|§\d+§|\w+(?:[’']\w+)?|[^\w\s]", processed_text)
    return final_tokens, specials

def weighted_frequencies(tokens):
    freq = {}
    for i, token in enumerate(tokens):
        boost = 2 if i < 100 else 1
        if token.istitle():
            boost += 1
        if len(token.strip()) > 6:
            boost += 1
        freq[token] = freq.get(token, 0) + boost
    return freq