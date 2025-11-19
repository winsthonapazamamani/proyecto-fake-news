import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import sys
import os

sys.path.append('src')

from data_preprocessing import DataPreprocessor

class ModelTester:
    def __init__(self, model_path, tokenizer_path):
        self.model = load_model(model_path)
        self.preprocessor = DataPreprocessor()
        self.preprocessor.load_tokenizer(tokenizer_path)
    
    def predict_single_text(self, text):
        """
        Predecir una sola noticia
        """
        processed_text = self.preprocessor.preprocess_text(text)
        sequences = self.preprocessor.tokenizer.texts_to_sequences([processed_text])
        X = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=self.preprocessor.max_len)
        
        prediction = self.model.predict(X)[0][0]
        label = "Verdadera" if prediction > 0.5 else "Falsa"
        confidence = prediction if prediction > 0.5 else 1 - prediction
        
        return {
            'text': text,
            'processed_text': processed_text,
            'prediction': label,
            'confidence': float(confidence),
            'raw_score': float(prediction)
        }
    
    def predict_batch(self, texts):
        """
        Predecir múltiples noticias
        """
        results = []
        for text in texts:
            result = self.predict_single_text(text)
            results.append(result)
        
        return pd.DataFrame(results)

def main():
    # Configuración
    MODEL_PATH = "models/trained_models/fake_news_model.h5"
    TOKENIZER_PATH = "models/trained_models/tokenizer.pkl"
    
    # Verificar que los archivos existan
    if not os.path.exists(MODEL_PATH) or not os.path.exists(TOKENIZER_PATH):
        print("Error: Modelo o tokenizer no encontrados. Ejecuta train_model.py primero.")
        return
    
    # Cargar tester
    tester = ModelTester(MODEL_PATH, TOKENIZER_PATH)
    
    # Ejemplos de prueba
    test_texts = [
        "El gobierno anuncia nuevas medidas economicas para estimular el crecimiento",
        "Alienigenas visitan la tierra en secreto segun fuentes militares",
        "Estudio cientifico confirma los beneficios del ejercicio regular",
        "Teoria de conspiracion sobre vacunas que cambian el ADN humano"
    ]
    
    print("Realizando predicciones de prueba...")
    results = tester.predict_batch(test_texts)
    
    # Mostrar resultados
    print("\nResultados de las predicciones:")
    print("=" * 80)
    for _, row in results.iterrows():
        print(f"Texto: {row['text'][:100]}...")
        print(f"Procesado: {row['processed_text'][:100]}...")
        print(f"Prediccion: {row['prediction']} (Confianza: {row['confidence']:.4f})")
        print("-" * 80)

if __name__ == "__main__":
    main()