import os
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# === Constants ===
MAXLEN = 100
LIST_CLASSES = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]


# === Model Class ===
class ToxicCommentClassifier:
    def __init__(self):
        """
        Initializes the classifier by loading the model and tokenizer.
        The model files are stored inside the 'models/' directory.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))  # Get package directory
        model_path = os.path.join(base_path, "models", "model.h5")
        tokenizer_path = os.path.join(base_path, "models", "tokenizer.pickle")

        # Load Tokenizer
        with open(tokenizer_path, "rb") as handle:
            self.tokenizer = pickle.load(handle)

        # Load Model
        self.model = load_model(model_path)

    def classify(self, text: str) -> dict:
        """
        Classifies a given text and returns toxicity scores.

        :param text: Input text to classify
        :return: Dictionary with toxicity scores
        """
        # Preprocess text
        seq = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=MAXLEN)

        # Predict toxicity scores
        preds = self.model.predict(padded)[0]

        # Return results as a dictionary
        return {LIST_CLASSES[i]: float(preds[i]) for i in range(len(LIST_CLASSES))}
