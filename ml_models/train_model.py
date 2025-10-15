import pandas as pd
from prediction_model import NewsPredictionModel
import os

def load_training_data():
    """Carga datos de entrenamiento (ejemplo)"""
    # En un caso real, esto vendría de tu base de datos
    sample_data = {
        'texts': [
            "Breaking news: Stock market reaches all time high",
            "Company reports significant losses this quarter",
            "New technology breakthrough announced today",
            "Economic crisis affects multiple industries",
            "Positive earnings report surprises analysts"
        ],
        'labels': [1, 0, 1, 0, 1]  # 1: Positive, 0: Negative
    }
    return sample_data

def main():
    # Cargar datos
    data = load_training_data()
    
    # Entrenar modelo
    model = NewsPredictionModel()
    accuracy = model.train(data['texts'], data['labels'])
    
    # Guardar modelo
    model_path = 'ml_models/trained_models/news_prediction_model.pkl'
    model.save_model(model_path)
    
    print(f"Model trained with accuracy: {accuracy:.4f}")
    print(f"Model saved to: {model_path}")

if __name__ == "__main__":
    main()