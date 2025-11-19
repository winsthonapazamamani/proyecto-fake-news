import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os

class DataPreprocessor:
    def __init__(self, max_features=10000, max_len=200):
        self.max_features = max_features
        self.max_len = max_len
        self.tokenizer = None
        self._download_nltk_resources()
        self.stop_words = set(stopwords.words('spanish' if 'spanish' in stopwords.fileids() else 'english'))
    
    def _download_nltk_resources(self):
        """Descargar recursos de NLTK de forma robusta"""
        resources = [
            'stopwords',
            'punkt',
            'punkt_tab'
        ]
        
        for resource in resources:
            try:
                nltk.download(resource, quiet=True)
                print(f"✓ Recurso NLTK '{resource}' disponible")
            except Exception as e:
                print(f"⚠ Recurso NLTK '{resource}' no disponible: {e}")
    
    def simple_tokenize(self, text):
        """
        Tokenización simple sin dependencia de punkt_tab
        """
        # Dividir por espacios y filtrar palabras vacías
        tokens = text.split()
        # Filtrar caracteres especiales y palabras muy cortas
        tokens = [re.sub(r'[^a-zA-Záéíóúñü]', '', token.lower()) for token in tokens]
        tokens = [token for token in tokens if len(token) > 2 and token not in self.stop_words]
        return tokens
    
    def preprocess_text(self, text):
        """
        Preprocesamiento completo del texto - Versión robusta
        """
        if isinstance(text, float) or text is None:
            return ""
        
        try:
            # Convertir a minúsculas
            text = str(text).lower()
            
            # Eliminar URLs
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            
            # Eliminar menciones y hashtags
            text = re.sub(r'@\w+|#\w+', '', text)
            
            # Eliminar caracteres especiales pero mantener acentos
            text = re.sub(r'[^\w\sáéíóúñü]', '', text)
            
            # Eliminar números
            text = re.sub(r'\d+', '', text)
            
            # Eliminar espacios múltiples
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Tokenizar (usar método simple si word_tokenize falla)
            try:
                tokens = word_tokenize(text)
            except:
                tokens = self.simple_tokenize(text)
            
            # Filtrar stopwords y palabras muy cortas
            tokens = [word for word in tokens if word not in self.stop_words and len(word) > 2]
            
            return ' '.join(tokens)
            
        except Exception as e:
            print(f"Error en preprocesamiento: {e}")
            return ""
    
    def prepare_data(self, texts, labels, tokenizer=None):
        """
        Preparar datos para el modelo - Versión mejorada
        """
        print("Preprocesando textos...")
        processed_texts = []
        valid_labels = []
        
        for i, (text, label) in enumerate(zip(texts, labels)):
            processed = self.preprocess_text(text)
            if processed and len(processed.strip()) > 10:  # Filtrar textos muy cortos
                processed_texts.append(processed)
                valid_labels.append(label)
        
        print(f"Textos válidos después de preprocesamiento: {len(processed_texts)}/{len(texts)}")
        
        if len(processed_texts) == 0:
            raise ValueError("No hay textos válidos después del preprocesamiento")
        
        # Configurar tokenizer
        if tokenizer is None:
            self.tokenizer = Tokenizer(num_words=self.max_features, oov_token='<OOV>')
            self.tokenizer.fit_on_texts(processed_texts)
        else:
            self.tokenizer = tokenizer
        
        # Convertir a secuencias
        sequences = self.tokenizer.texts_to_sequences(processed_texts)
        
        # Padding
        X = pad_sequences(sequences, maxlen=self.max_len)
        
        # Convertir labels a numpy array
        y = np.array(valid_labels)
        
        return X, y, self.tokenizer
    
    def save_tokenizer(self, filepath):
        """Guardar tokenizer para uso futuro"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Tokenizer guardado en: {filepath}")
    
    def load_tokenizer(self, filepath):
        """Cargar tokenizer guardado"""
        with open(filepath, 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        return self.tokenizer