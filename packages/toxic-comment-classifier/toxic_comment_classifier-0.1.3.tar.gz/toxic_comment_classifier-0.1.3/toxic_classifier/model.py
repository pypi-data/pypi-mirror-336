import os
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from typing import List

# === Constants ===
MAXLEN = 100
LIST_CLASSES = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]


# === Model Class ===
class ToxicCommentClassifier:
    def __init__(self):
        """
        Initializes the classifier by loading the model and tokenizer.
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

    def predict(self, text: str) -> float:
        """
        Predicts a single toxicity score (average of all toxicity classes).

        :param text: Input text to classify
        :return: Average toxicity score (float)
        """
        scores = self.classify(text)
        return np.mean(list(scores.values()))

    def predict_batch(self, texts: List[str]) -> List[float]:
        """
        Predicts toxicity scores for a batch of texts.

        :param texts: List of input texts
        :return: List of average toxicity scores
        """
        scores_list = [self.classify(text) for text in texts]
        return [np.mean(list(scores.values())) for scores in scores_list]
