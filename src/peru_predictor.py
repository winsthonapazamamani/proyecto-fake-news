import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import pickle
import sys
import os

sys.path.append('src')

from data_preprocessing import DataPreprocessor
from peru_context import PeruContextEnhancer

class PeruNewsPredictor:
    def __init__(self, model_path, tokenizer_path):
        self.model = load_model(model_path)
        self.preprocessor = DataPreprocessor()
        self.preprocessor.load_tokenizer(tokenizer_path)
        self.context_enhancer = PeruContextEnhancer()
    
    def predict_news(self, text):
        """
        Predecir si una noticia peruana es falsa o verdadera
        """
        # Preprocesar texto
        processed_text = self.preprocessor.preprocess_text(text)
        
        if not processed_text or len(processed_text.strip()) < 10:
            return {
                'prediccion': 'NO_DETERMINADO',
                'confianza': 0.0,
                'error': 'Texto muy corto o no válido'
            }
        
        # Preparar datos para el modelo
        sequences = self.preprocessor.tokenizer.texts_to_sequences([processed_text])
        X = tf.keras.preprocessing.sequence.pad_sequences(
            sequences, maxlen=self.preprocessor.max_len
        )
        
        # Predicción base del modelo
        raw_prediction = self.model.predict(X, verbose=0)[0][0]
        base_prediction = 0 if raw_prediction < 0.5 else 1
        base_confidence = raw_prediction if base_prediction == 1 else 1 - raw_prediction
        
        # Mejorar con contexto peruano
        enhanced_result = self.context_enhancer.enhance_features(
            text, base_prediction, base_confidence
        )
        
        return {
            'noticia': text[:200] + "..." if len(text) > 200 else text,
            **enhanced_result,
            'prediccion_base': 'VERDADERA' if base_prediction == 1 else 'FALSA',
            'confianza_base': float(base_confidence)
        }
    
    def predict_batch(self, texts):
        """
        Predecir múltiples noticias
        """
        results = []
        for text in texts:
            result = self.predict_news(text)
            results.append(result)
        
        return pd.DataFrame(results)
    
    def analyze_trends(self, texts):
        """
        Analizar tendencias en un conjunto de noticias
        """
        predictions = self.predict_batch(texts)
        
        analysis = {
            'total_noticias': len(predictions),
            'noticias_verdaderas': len(predictions[predictions['prediccion'] == 'VERDADERA']),
            'noticias_falsas': len(predictions[predictions['prediccion'] == 'FALSA']),
            'confianza_promedio': predictions['confianza'].mean(),
            'temas_frecuentes': self._extract_frequent_topics(texts)
        }
        
        return analysis
    
    def _extract_frequent_topics(self, texts):
        """
        Extraer temas frecuentes de las noticias
        """
        all_text = ' '.join(texts).lower()
        topics = {}
        
        for category, keywords in self.context_enhancer.peru_keywords.items():
            for keyword in keywords:
                if keyword in all_text:
                    count = all_text.count(keyword)
                    if count > 0:
                        topics[keyword] = count
        
        # Ordenar por frecuencia
        return dict(sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10])