import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pandas as pd
from word_embedding import get_vector_by_word
from create_ngram_lm import create_vocab_from_df

if __name__ == '__main__':
    lm = keras.Sequential(
        [
            keras.Input(shape=(1, 300)),
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

    x = tf.ones((1, 300))
    y = lm(x)
    print(y)
    print(lm.summary())

    # df = pd.read_csv('data.csv')
    # vocab = create_vocab_from_df(df)
    # our_words = list(vocab)[1:10]
    # train_bigrams = []
    # for i in range(0, 10):
    #     for j in range(0, 10):
    #         train_bigrams.append(our_words[i] + our_words[j])
    #
    # print(train_bigrams)

    X_train = np.array([get_vector_by_word('я'),
                        get_vector_by_word('пошел'),
                        get_vector_by_word('домой')])
    print(X_train)
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

    Y_train = np.random.random((1,))
    print(Y_train)

    lm.compile(optimizer=optimizer, loss=loss_function, metrics=[metrics])

    lm.fit(X_train, Y_train, batch_size=5, epochs=100)
