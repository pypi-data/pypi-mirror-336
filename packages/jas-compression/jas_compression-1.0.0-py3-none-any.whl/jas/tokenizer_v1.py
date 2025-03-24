import re

def smart_tokenize(text):
    # Step 1: Capture all tokens including whitespace and punctuation
    # Preserve apostrophes properly (like you’ve)
    tokens = re.findall(r"\s+|\w+(?:[’']\w+)?|[.,!?;:()\"']", text)
    return tokens

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
