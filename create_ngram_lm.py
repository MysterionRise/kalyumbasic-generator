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
    uningram_model = BaseLM(1, list(vocab))
    bigram_model = BaseLM(2, list(vocab))
    trigram_model = BaseLM(3, list(vocab))
    train, test, val = train_test_validate_split(generate_sentences(df))
    # train ngram model
    nlp = Russian()
    for sent in train:
        doc = nlp(sent.text.lower())
        tokens = []
        for token in doc:
            cleaned_token = normalise_and_cleanup(token.text)
            if len(cleaned_token) > 0:
                tokens.append(cleaned_token)
        bigram_model.update(tokens)

    # print(bigram_model.ngrams)
    print(bigram_model.perplexity(['чего', 'ты', 'сидишь', 'здесь']))
