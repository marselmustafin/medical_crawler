import sys
import json
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')

with open(sys.argv[1]) as crawled_data:
    docs = json.load(crawled_data)

    contents = [doc["content"]
                for doc in docs if doc["content"] is not None]
    pos_contents = [doc["pos_content"]
                    for doc in docs if doc["pos_content"] is not None]
    neg_contents = [doc["neg_content"]
                    for doc in docs if doc["neg_content"] is not None]
    all_contents = contents + pos_contents + neg_contents

    tokens = []
    for sentence in all_contents:
        temp_tokens = tokenizer.tokenize(sentence)
        for token in temp_tokens:
            tokens.append(token)

    tokens = [token.lower() for token in tokens]
    unique_tokens = set(tokens)

    print("===== STATISTCS ======")
    print("Docs count: ".ljust(30), len(docs))
    print("Contents overall: ".ljust(30), len(all_contents))
    print("Neutral contents: ".ljust(30), len(contents))
    print("Positive contents: ".ljust(30), len(pos_contents))
    print("Negative contents: ".ljust(30), len(neg_contents))
    print("Words overall: ".ljust(30), len(tokens))
    print("Unique words: ".ljust(30), len(unique_tokens))
