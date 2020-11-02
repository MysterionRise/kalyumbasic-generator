import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

import word_embedding
import pandas as pd
from create_ngram_lm import create_vocab_from_df, generate_sentences, generate_tokens_from_sentence, \
    train_test_validate_split


def calcProb(i: int, j: int, k: int):
    if i + 1 == j and j + 1 == k:
        return 1.0
    return 0.0


if __name__ == '__main__':
    lm = keras.Sequential(
        [
            keras.Input(shape=(1, 900)),
            layers.Dense(24, activation='softplus'),
            layers.Dense(100, activation='softplus'),
            layers.Dense(16, activation='softplus'),
            layers.Dense(1, activation='softmax'),
            # layers.Softmax()
        ],
        name="lm",
    )

    optimizer = keras.optimizers.Adam()

    loss_function = keras.losses.CategoricalCrossentropy()

    metrics = keras.metrics.CategoricalAccuracy()

    df = pd.read_csv('data.csv')
    vocab = create_vocab_from_df(df)
    train_sents, test_sents, val_sents = train_test_validate_split(generate_sentences(df), train_ratio=0.01)
    train_trigrams = []
    train_prob = []
    # itertools
    # generate triples, and check if it exists in train_trigrams
    # token empty
    for sent in train_sents:
        tokens = generate_tokens_from_sentence(sent)
        print(tokens)
        tokens_len = len(tokens)
        for i in range(0, tokens_len - 2):
            train_trigrams.append((tokens[i], tokens[i + 1], tokens[i + 2]))
            train_prob.append(1.0)

        # print(train_trigrams)
        # print(train_prob)
    # x = [(i, i + 1, i + 2) for i in range(0, len(l)) if i + 2 <= len(l)]
    # [x for w in word_sentences ]
    X_train = [word_embedding.get_vector_by_words(list(gram)).reshape((900, 1)).T for gram in train_trigrams]
    Y_train = train_prob
    print(X_train.shape)
    # print(X.shape)
    # X_train = X.reshape((900, 1)).T
    # print(X_train.shape)
    # [я пошел]
    # X - [0 0 0 0 0 0 1] [0 0 0 0 0 0 1 0 0 0 0 0]

    # Y - [домой]
    # [ 0 0 0 0 1 0 0 0 0 0 ]

    # [0.0001 0.0001 0.900 0.]
    # get max
    # check loaders

    # я пошел домой. погода была прекрасная
    # я пошел
    # пошел домой
    # домой </s>
    # <s> погода

    # Y_train = np.random.random((1, 1))
    # print(Y_train)
    #
    lm.compile(optimizer=optimizer, loss=loss_function, metrics=[metrics])
    #
    lm.fit(X_train, Y_train, batch_size=5, epochs=100)
