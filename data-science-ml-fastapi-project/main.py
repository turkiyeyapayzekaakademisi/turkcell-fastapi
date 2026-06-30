from fastapi import FastAPI
import pandas as pd
from pathlib import Path
import json
from pydantic import BaseModel, Field
import joblib

app = FastAPI(title = "Iris veri Analizi API")

DATA_PATH = Path("data.json")
MODEL_PATH = Path("models") / "iris_decision_tree_model.joblib"

class IrisInput(BaseModel):
    sepal_length: float = Field(..., gt = 0, description="Sepal Uzunluğu")
    sepal_width: float = Field(..., gt = 0, description="Sepal Genişliği")
    petal_length: float = Field(..., gt = 0, description="Petal Uzunluğu")
    petal_width: float = Field(..., gt = 0, description="Petal Genişliği")

def load_dataset():
    """data.json okur ve pandas dataframe e çevirir."""

    df = pd.read_json(DATA_PATH)

    return df

df = load_dataset()
print(df.head())

def dataframe_to_json(data):
    return json.loads(data.to_json())

print(dataframe_to_json(df))

@app.get("/")
def home():
    return {
        "message": "Iris veri analizi api çalışıyor."
    }

@app.get("/data")
def read_data():
    """veri setini okur ve ilk 5 satırı döndürür"""

    df = load_dataset()

    return {
        "message": "Veri seti başarıyla okundu",
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "first_5_rows": df.head().to_dict()
    }

@app.get("/analysis")
def analyze_dataset():
    """Veri seti için temel istatistiksel analiz"""

    df = load_dataset()

    numeric_columns = df.select_dtypes(include = ["int64", "float64"]).columns.tolist()
    categorical_columns = df.select_dtypes(include = ["object"]).columns.tolist()

    missing_values = df.isnull().sum().to_dict()

    numeric_summary = df[numeric_columns].describe().to_dict()

    analysis_result = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "missing_values": missing_values,
        "species_distribution": df["species"].value_counts().to_dict(),
        "numeric_summary": numeric_summary 
    }

    return analysis_result

def load_model():
    model_artifact = joblib.load(MODEL_PATH)
    return model_artifact

@app.post("/predict")
def predict_species(input_data: IrisInput):
    """Eğitilmiş karar ağacı modelini kullanarak iris türü tahmini yapar"""

    model_artifact = load_model()
    model = model_artifact["model"]
    feature_columns = model_artifact["feature_columns"]

    input_df = pd.DataFrame(
        [
            {
                "sepal_length": input_data.sepal_length, 
                "sepal_width": input_data.sepal_width, 
                "petal_length": input_data.petal_length, 
                "petal_width": input_data.petal_width, 
            }
        ]
    )

    input_df = input_df[feature_columns]

    prediction = model.predict(input_df)[0]

    return {
        "message": "tahmin başarıyla yapıldı",
        "prediction": prediction
    }