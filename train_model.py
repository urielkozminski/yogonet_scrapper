import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import os

def train_multiclass_classifier(csv_path: str):
    df = pd.read_csv(csv_path)

    if 'text_or_url' not in df.columns or 'label' not in df.columns:
        raise ValueError("El CSV debe tener columnas: 'text_or_url' y 'label'")

    X = df['text_or_url'].astype(str)
    y = df['label'].astype(str)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", RandomForestClassifier(n_estimators=200, random_state=42)),
    ])

    pipeline.fit(X, y)

    os.makedirs("model_assets", exist_ok=True)
    joblib.dump(pipeline, "model_assets/element_classifier.pkl")
    print("Modelo guardado en model_assets/element_classifier.pkl")

if __name__ == "__main__":
    train_multiclass_classifier("training_data/dataset.csv")