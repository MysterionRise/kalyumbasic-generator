import markovify
import pandas as pd
import numpy as np
import pickle


def generate_model():
    data = pd.read_csv('data.csv')
    data = data.replace(np.nan, '', regex=True)

    text = '\n'.join(data['text'].values.tolist())
    text = text.replace(".", "\n")

    # Build the model.
    text_model = markovify.NewlineText(text)
    with open('model.data', 'wb') as f:
        pickle.dump(text_model, f)


if __name__ == "__main__":
    generate_model()
