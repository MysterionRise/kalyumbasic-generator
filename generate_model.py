import pickle
import re

import markovify
import numpy as np
import pandas as pd


def generate_source_text():
    data = pd.read_csv("data.csv")
    data.dropna(inplace=True)

    split_lines = [line.splitlines() for line in data["text"].values.tolist()]
    lines = np.concatenate(split_lines)
    bad_chars = r"\s|-|—|_"
    lines = [re.sub(r"\[.+\]", "", line) for line in lines]
    lines = [re.sub(f"^({bad_chars})+|({bad_chars})+$", "", line) for line in lines]
    lines = [line[0].lower() + line[1:] for line in lines if line.strip()]

    text = "\n".join(lines)
    return text


def generate_model():
    text = generate_source_text()

    # Build the model
    text_model = markovify.NewlineText(text, well_formed=False)
    with open("model.data", "wb") as f:
        pickle.dump(text_model, f)

    with open("model.data", "rb") as f:
        model = pickle.load(f)

    for _ in range(1, 20):
        print(model.make_sentence())


if __name__ == "__main__":
    generate_model()
