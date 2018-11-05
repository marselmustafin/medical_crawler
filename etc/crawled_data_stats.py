import sys
import json
import math
from string import punctuation
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

WORD_REGEXP = r'[а-яА-Яa-zA-Z]+'
tokenizer = RegexpTokenizer(WORD_REGEXP)
# vectorizer = TfidfVectorizer(token_pattern=WORD_REGEXP)


def flat_list(list_of_lists):
    return [y for x in list_of_lists for y in x]


def tokened_sentences(docs):
    tokened_sentences = []
    for sentence in all_texts:
        tokened_sentence = [
            token.lower() for token in tokenizer.tokenize(sentence)]
        tokened_sentences.append(tokened_sentence)
    return tokened_sentences


with open(sys.argv[1]) as crawled_data:
    items = json.load(crawled_data)

    year_counts = Counter()
    rate_counts = Counter()

    for item in items:
        rate_counts[item["avg_rate"]] += 1
        year_counts[item["year"]] += 1

    contents = [item["content"]
                for item in items if item["content"] is not None]
    pos_contents = [item["pos_content"]
                    for item in items if item["pos_content"] is not None]
    neg_contents = [item["neg_content"]
                    for item in items if item["neg_content"] is not None]
    replies = [item["reply"]
               for item in items if item["reply"] is not None]

    all_texts = contents + pos_contents + neg_contents + replies

    tokened_sentences = tokened_sentences(all_texts)
    tokens = flat_list(tokened_sentences)
    unique_tokens = set(tokens)
    # tf_idf_matrix = vectorizer.fit_transform(all_texts)

    print("===== STATISTICS ======")
    print("Items count: ".ljust(30), len(items))
    print("Texts overall: ".ljust(30), len(all_texts))
    print("Neutral contents: ".ljust(30), len(contents))
    print("Positive contents: ".ljust(30), len(pos_contents))
    print("Negative contents: ".ljust(30), len(neg_contents))
    print("Replies: ".ljust(30), len(replies))
    print("Words overall: ".ljust(30), len(tokens))
    print("Unique words: ".ljust(30), len(unique_tokens))
    print("======================")
    for year, count in sorted(year_counts.items()):
        print("Docs with", year, "year:", count)
    print("======================")
    for rate, count in sorted(rate_counts.items()):
        print("Docs with rate", rate, ":", count)
    # print("===TF====IDF====TF-IDF====")
    # print(tf_idf_matrix)
