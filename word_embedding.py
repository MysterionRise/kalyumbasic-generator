from gensim.models import KeyedVectors
import numpy as np
from nltk import pos_tag, word_tokenize
from spacy.lang.ru import Russian

model = KeyedVectors.load_word2vec_format('models/ruscorpora_upos_cbow_300_20_2019/model.bin', binary=True)

nlp = Russian()

MAPPINGS = {
    "A": "ADJ",
    "A-PRO": "PRON",
    "ADV": "ADV",
    "ADV-PRO": "PRON",
    "ANUM": "ADJ",
    "CONJ": "CONJ",
    "INTJ": "X",
    "NONLEX": ".",
    "NUM": "NUM",
    "PARENTH": "PRT",
    "PART": "PRT",
    "PR": "ADP",
    "PRAEDIC": "PRT",
    "PRAEDIC-PRO": "PRON",
    "S": "NOUN",
    "S-PRO": "PRON",
    "V": "VERB",
}


def lemmatization(text):
    doc = nlp(text)
    for token in doc:
        print(token, token.lemma, token.lemma_)
    tokens = [token.lemma_ for token in doc]
    return " ".join(tokens)


def get_vector_by_word(word: str):
    doc = nlp(word)
    token = doc[0]
    lemma = token.lemma_
    pos = pos_tag(word_tokenize(lemma), lang='rus')[0][1]
    try:
        converted_pos = MAPPINGS.get(pos)
        key = '{}_{}'.format(lemma, converted_pos)
        value = model.get_vector(key)
        # print(value)
        return value
    except KeyError:
        print('{} or {} not found in model'.format(key, pos))
    return np.ones((300,))


def get_vector_by_words(words):
    return np.append(get_vector_by_word(words[0]), [get_vector_by_word(w) for w in words[1:]])


if __name__ == '__main__':
    print(get_vector_by_words('я', 'пошел', 'домой').shape)
