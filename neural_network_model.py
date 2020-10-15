import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

import word_embedding

# from create_ngram_lm import create_vocab_from_df

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

    # df = pd.read_csv('data.csv')
    # vocab = create_vocab_from_df(df)
    # our_words = list(vocab)[1:10]
    # train_bigrams = []
    # for i in range(0, 10):
    #     for j in range(0, 10):
    #         train_bigrams.append(our_words[i] + our_words[j])
    #
    # print(train_bigrams)
    # x = [(i, i + 1, i + 2) for i in range(0, len(l)) if i + 2 <= len(l)]
    [x for w in word_sentences ]
    X = word_embedding.get_vector_by_words('я', 'пошел', 'домой')
    print(X.shape)
    X_train = X.reshape((900, 1)).T
    print(X_train.shape)
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

    Y_train = np.random.random((1, 1))
    print(Y_train)
    #
    lm.compile(optimizer=optimizer, loss=loss_function, metrics=[metrics])
    #
    lm.fit(X_train, Y_train, batch_size=5, epochs=100)
