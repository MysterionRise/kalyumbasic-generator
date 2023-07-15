import logging
import pickle
import re

import markovify
import numpy as np
import pandas as pd

DATA_PATH = "data.csv"
MODEL_PATH = "model.data"
BAD_CHARS = r"\\s|-|—|_"
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def generate_source_text(data_path):
    """Generate source text from a CSV file."""
    data = pd.read_csv(data_path)
    data.dropna(inplace=True)

    split_lines = [line.splitlines() for line in data["text"].values.tolist()]
    lines = np.concatenate(split_lines)
    lines = [re.sub(r"\\[.+\\]", "", line) for line in lines]
    lines = [re.sub(f"^({BAD_CHARS})+|({BAD_CHARS})+$", "", line) for line in lines]
    lines = [line[0].lower() + line[1:] for line in lines if line.strip()]

    return "\n".join(lines)


def generate_model(text, model_path):
    """Generate a Markov model from the source text and save it to a file."""
    text_model = markovify.NewlineText(text, well_formed=False)
    with open(model_path, "wb") as f:
        pickle.dump(text_model, f)

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    for _ in range(1, 20):
        logging.info(model.make_sentence())


if __name__ == "__main__":
    text = generate_source_text(DATA_PATH)
    generate_model(text, MODEL_PATH)
