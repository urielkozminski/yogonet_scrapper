import logging
from bs4 import Tag
import joblib

MODEL_PATH = "model_assets/element_classifier.pkl"

class AIPredictor:
    def __init__(self):
        try:
            with open(MODEL_PATH, "rb") as f:
                self.pipeline = joblib.load(f) 
        except Exception as e:
            logging.error(f"Error loading model pipeline: {e}")
            raise

    def predict_element_type(self, element: Tag) -> str:
        text = element.get_text(strip=True)
        if not text:
            return "unknown"

        try:
            prediction = self.pipeline.predict([text])[0]
            return prediction
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            return "unknown"

_predictor_instance = None

def get_predictor() -> AIPredictor:
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = AIPredictor()
    return _predictor_instance

def predict_element_type(element: Tag) -> str:
    predictor = get_predictor()
    return predictor.predict_element_type(element)
