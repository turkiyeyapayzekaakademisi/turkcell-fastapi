from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

DATA_PATH = Path("data.json")
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "iris_decision_tree_model.joblib"

def load_dataset():

    return pd.read_json(DATA_PATH)

def train_model():
    """İris veri seti ile karar ağacı modeli eğit"""

    df = load_dataset()

    feature_columns = [
        "sepal_length", 
        "sepal_width",
        "petal_length",
        "petal_width"
    ]

    target_column = "species"

    X = df[feature_columns]
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)

    print(classification_report(y_test, y_pred))

    MODEL_DIR.mkdir(exist_ok=True)

    model_artifact = {
        "model": model,
        "feature_columns": feature_columns,
        "target_column": target_column,
        "classes": sorted(y.unique().tolist())
    }

    joblib.dump(model_artifact, MODEL_PATH)

if __name__ == "__main__":
    train_model()

