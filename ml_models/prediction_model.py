import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from utils.text_preprocessor import TextPreprocessor

class NewsPredictionModel:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.preprocessor = TextPreprocessor()
        
    def preprocess_data(self, texts):
        """Preprocesa los textos para el entrenamiento"""
        processed_texts = [self.preprocessor.clean_text(text) for text in texts]
        return processed_texts
    
    def train(self, texts, labels, test_size=0.2):
        """Entrena el modelo con los datos proporcionados"""
        # Preprocesamiento
        processed_texts = self.preprocess_data(texts)
        
        # Vectorización
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        X = self.vectorizer.fit_transform(processed_texts)
        y = np.array(labels)
        
        # División train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Entrenamiento
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluación
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model accuracy: {accuracy:.4f}")
        print(classification_report(y_test, y_pred))
        
        return accuracy
    
    def predict(self, text):
        """Realiza predicción sobre un nuevo texto"""
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model not trained. Call train() first.")
        
        processed_text = self.preprocessor.clean_text(text)
        X = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0]
        
        return {
            'prediction': int(prediction),
            'confidence': float(max(probability)),
            'probabilities': {
                'class_0': float(probability[0]),
                'class_1': float(probability[1])
            }
        }
    
    def save_model(self, model_path):
        """Guarda el modelo entrenado"""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'vectorizer': self.vectorizer
        }, model_path)
    
    def load_model(self, model_path):
        """Carga un modelo pre-entrenado"""
        if os.path.exists(model_path):
            loaded = joblib.load(model_path)
            self.model = loaded['model']
            self.vectorizer = loaded['vectorizer']
        else:
            raise FileNotFoundError(f"Model file not found: {model_path}")