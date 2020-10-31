from typing import Set, List, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split
from spacy.lang.ru import Russian
import re

from base_language_model import BaseLM


def normalise_and_cleanup(token: str):
    bad_chars = r'\s|-|—|_'
    token = re.sub(r'\[.+\]', '', token)
    token = re.sub(f'^({bad_chars})+|({bad_chars})+$', '', token)
    return token


def create_vocab_from_df(df) -> Set[str]:
    vocab = set()
    nlp = Russian()
    for index, row in df.iterrows():
        try:
            doc = nlp(row['text'].lower())
            for token in doc:
                if len(token.text) > 0:
                    vocab.add(normalise_and_cleanup(token.text))
        except AttributeError:
            print(row['text'])

    vocab.add('<s>')
    vocab.add('</s>')
    return vocab


def generate_sentences(df) -> List[str]:
    nlp = Russian()
    sentencizer = nlp.create_pipe("sentencizer")
    nlp.add_pipe(sentencizer)
    all_sentences = []
    for index, row in df.iterrows():
        try:
            doc = nlp(row['text'].lower())
            all_sentences.extend(doc.sents)
        except:
            print(row['text'])
    return all_sentences


def generate_tokens_from_sentences(sentenses: List) -> List[str]:
    res_tokens = []
    for sent in sentenses:
        res_tokens.extend(generate_tokens_from_sentence(sent))
    return res_tokens


def generate_tokens_from_sentence(sent) -> List[str]:
    nlp = Russian()
    tokens = []
    doc = nlp(sent.text.lower())
    tokens.append('<s>')
    for token in doc:
        cleaned_token = normalise_and_cleanup(token.text)
        if len(cleaned_token) > 0:
            tokens.append(cleaned_token)
    tokens.append('</s>')
    return tokens


def train_test_validate_split(sentences: List[str], train_ratio: float = 0.8, validation_ratio: float = 0.1,
                              test_ratio: float = 0.1) -> Tuple[List[str], List[str], List[str]]:
    train, test = train_test_split(sentences, test_size=1 - train_ratio)

    val, test = train_test_split(test, test_size=test_ratio / (test_ratio + validation_ratio))

    print(len(sentences))
    print(len(train))
    print(len(val))
    print(len(test))
    return train, test, val


if __name__ == "__main__":
    df = pd.read_csv('data.csv')
    vocab = create_vocab_from_df(df)
    uningram_model = BaseLM(1, k=2, vocab=list(vocab))
    bigram_model = BaseLM(2, k=2, vocab=list(vocab))
    trigram_model = BaseLM(3, k=2, vocab=list(vocab))
    fourgram_model = BaseLM(4, k=2, vocab=list(vocab))
    train, test, val = train_test_validate_split(generate_sentences(df))
    # train ngram model
    for sent in train:
        tokens = generate_tokens_from_sentence(sent)
        fourgram_model.update(tokens)
        trigram_model.update(tokens)
        bigram_model.update(tokens)
        uningram_model.update(tokens)

    tokens = generate_tokens_from_sentences(val[0:1])
    print(uningram_model.perplexity(tokens))
    print(bigram_model.perplexity(tokens))
    print(trigram_model.perplexity(tokens))
    print(fourgram_model.perplexity(tokens))

    print(uningram_model.generate_text(10))
    print(bigram_model.generate_text(10))
    print(trigram_model.generate_text(10))
    print(fourgram_model.generate_text(10))


