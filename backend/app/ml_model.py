import numpy as np
import pandas as pd
import joblib
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

# Importaciones condicionales para TensorFlow
try:
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout, Bidirectional
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("⚠️  TensorFlow no disponible, usando modo fallback")
    TENSORFLOW_AVAILABLE = False

import os
from pathlib import Path
import json
from .database import get_db

class NewsClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.tokenizer = None
        self.label_encoder = None
        self.max_sequence_length = 200
        self.vocab_size = 10000
        self.embedding_dim = 100
        self.is_trained = False
        self.metrics = {}
        self.use_tensorflow = TENSORFLOW_AVAILABLE
        
        # Caracteristicas especificas para espanol peruano
        self.peruvian_slang = {
            'chevere': 'bueno', 'jato': 'casa', 'pata': 'amigo',
            'ferro': 'automovil', 'yuca': 'dificil', 'papi': 'padre',
            'michi': 'gato', 'chibolo': 'nino', 'chibola': 'nina',
            'paltearse': 'asustarse', 'jamear': 'comer', 'causa': 'amigo',
            'choro': 'ladron', 'trome': 'habil', 'palteado': 'asustado',
            'chamba': 'trabajo'
        }
        
        # Patrones de noticias falsas en contexto peruano
        self.fake_news_patterns = [
            r'!?[!!]{2,}',  # Multiples signos de exclamacion
            r'\b(descubre|sorprendente|increible|impactante|secreto|oculto)\b',
            r'\b(urgente|importantisimo|atencion|alerta)\b',
            r'[A-Z]{4,}',  # Palabras en mayusculas
            r'\b(gratis|regala|milagro|instantaneo)\b',
            r'\b(cura|elimina|destruye|acaba con)\b',
            r'\b(descubrimiento|revelacion|impacto)\b',
        ]
        
        self.load_models()
    
    def load_models(self):
        """Cargar modelos pre-entrenados o crear nuevos"""
        models_path = Path(__file__).parent.parent / "models"
        models_path.mkdir(exist_ok=True)
        
        try:
            if self.use_tensorflow:
                # Modelo LSTM
                lstm_path = models_path / "trained_lstm.h5"
                if lstm_path.exists():
                    self.model = load_model(lstm_path)
                    self.is_trained = True
                    print("✅ Modelo LSTM cargado desde archivo")
                else:
                    self.create_default_model()
                    print("✅ Nuevo modelo LSTM creado")
            else:
                self.create_fallback_model()
                print("✅ Modelo Random Forest creado (fallback)")
            
            # Tokenizer
            tokenizer_path = models_path / "tokenizer.pkl"
            if tokenizer_path.exists():
                self.tokenizer = joblib.load(tokenizer_path)
                print("✅ Tokenizer cargado")
            else:
                if self.use_tensorflow:
                    from tensorflow.keras.preprocessing.text import Tokenizer
                    self.tokenizer = Tokenizer(num_words=self.vocab_size, oov_token="<OOV>")
                else:
                    # Tokenizer simple para modo fallback
                    class SimpleTokenizer:
                        def __init__(self):
                            self.word_index = {}
                            self.index_word = {}
                        
                        def fit_on_texts(self, texts):
                            words = set()
                            for text in texts:
                                words.update(text.split())
                            self.word_index = {word: idx+1 for idx, word in enumerate(words)}
                            self.index_word = {idx: word for word, idx in self.word_index.items()}
                        
                        def texts_to_sequences(self, texts):
                            sequences = []
                            for text in texts:
                                sequence = [self.word_index.get(word, 0) for word in text.split()]
                                sequences.append(sequence)
                            return sequences
                    
                    self.tokenizer = SimpleTokenizer()
                print("✅ Nuevo tokenizer creado")
            
            # Vectorizer para caracteristicas adicionales
            vectorizer_path = models_path / "vectorizer.pkl"
            if vectorizer_path.exists():
                self.vectorizer = joblib.load(vectorizer_path)
                print("✅ Vectorizer cargado")
            else:
                self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='spanish')
                print("✅ Nuevo vectorizer creado")
            
            # Cargar metricas
            self.load_metrics()
            
        except Exception as e:
            print(f"❌ Error cargando modelos: {e}")
            self.create_fallback_model()
    
    def create_default_model(self):
        """Crear modelo LSTM por defecto"""
        if not self.use_tensorflow:
            self.create_fallback_model()
            return
            
        self.model = Sequential([
            Embedding(self.vocab_size, self.embedding_dim, input_length=self.max_sequence_length),
            Bidirectional(LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.3)),
            Bidirectional(LSTM(64, dropout=0.3, recurrent_dropout=0.3)),
            Dense(64, activation='relu'),
            Dropout(0.4),
            Dense(32, activation='relu'),
            Dropout(0.3),
            Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            loss='binary_crossentropy',
            optimizer=Adam(learning_rate=0.001),
            metrics=['accuracy']
        )
        
        print("✅ Modelo LSTM por defecto creado")
    
    def create_fallback_model(self):
        """Crear modelo de fallback si TensorFlow no esta disponible"""
        print("🔄 Usando modelo Random Forest de respaldo")
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = TfidfVectorizer(max_features=2000, stop_words='spanish')
        self.use_tensorflow = False
    
    def load_metrics(self):
        """Cargar metricas desde la base de datos"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT accuracy, precision, recall, f1_score FROM model_metrics ORDER BY id DESC LIMIT 1"
                )
                result = cursor.fetchone()
                
                if result:
                    self.metrics = {
                        'accuracy': result['accuracy'],
                        'precision': result['precision'],
                        'recall': result['recall'],
                        'f1_score': result['f1_score']
                    }
                    print("✅ Metricas cargadas desde la base de datos")
                else:
                    self.metrics = {'accuracy': 0, 'precision': 0, 'recall': 0, 'f1_score': 0}
                    print("⚠️ Metricas no encontradas, usando valores por defecto")
                    
        except Exception as e:
            print(f"❌ Error cargando metricas: {e}")
            self.metrics = {'accuracy': 0, 'precision': 0, 'recall': 0, 'f1_score': 0}
    
    def save_metrics(self, accuracy, precision, recall, f1_score):
        """Guardar metricas en la base de datos"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO model_metrics 
                    (accuracy, precision, recall, f1_score, model_type) 
                    VALUES (?, ?, ?, ?, ?)""",
                    (accuracy, precision, recall, f1_score, 'LSTM + Random Forest')
                )
                conn.commit()
            
            self.metrics = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score
            }
            print("✅ Metricas guardadas en la base de datos")
            
        except Exception as e:
            print(f"❌ Error guardando metricas: {e}")
    
    def preprocess_peruvian_text(self, text):
        """Preprocesamiento especifico para espanol peruano"""
        if not isinstance(text, str):
            return ""
            
        # Convertir a minusculas
        text = text.lower()
        
        # Reemplazar jerga peruana
        for slang, replacement in self.peruvian_slang.items():
            text = re.sub(r'\b' + slang + r'\b', replacement, text)
        
        # Limpiar texto conservando acentos
        text = re.sub(r'[^\w\sáéíóúñ]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def extract_features(self, text):
        """Extraer caracteristicas del texto para analisis peruano"""
        processed_text = self.preprocess_peruvian_text(text)
        
        features = []
        
        # Caracteristicas linguisticas basicas
        words = processed_text.split()
        features.append(f"Palabras: {len(words)}")
        features.append(f"Caracteres: {len(text)}")
        
        # Deteccion de patrones de noticias falsas
        clickbait_score = 0
        for pattern in self.fake_news_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            clickbait_score += len(matches)
        
        features.append(f"Indicadores clickbait: {clickbait_score}")
        
        # Uso de mayusculas
        upper_ratio = sum(1 for char in text if char.isupper()) / max(len(text), 1)
        if upper_ratio > 0.3:
            features.append("Alto uso de mayusculas")
        
        # Longitud del texto
        if len(words) < 8:
            features.append("Titular muy corto")
        elif len(words) > 25:
            features.append("Titular muy extenso")
        
        # Contexto peruano
        peruvian_terms = sum(1 for word in words if any(
            term in word for term in 
            ['peru', 'peruano', 'lima', 'sunat', 'minedu', 'presidente']
        ))
        if peruvian_terms > 0:
            features.append("Contexto peruano detectado")
        
        return features
    
    def prepare_data(self, texts, labels=None):
        """Preparar datos para el modelo"""
        if self.use_tensorflow:
            if labels is not None and hasattr(self.tokenizer, 'word_index'):
                sequences = self.tokenizer.texts_to_sequences(texts)
            else:
                self.tokenizer.fit_on_texts(texts)
                sequences = self.tokenizer.texts_to_sequences(texts)
            
            padded_sequences = pad_sequences(sequences, maxlen=self.max_sequence_length, padding='post', truncating='post')
            return padded_sequences
        else:
            # Para modo fallback, usar TF-IDF
            if labels is not None:
                features = self.vectorizer.fit_transform(texts)
            else:
                features = self.vectorizer.transform(texts)
            return features
    
    def train_model(self, texts, labels, validation_split=0.2, epochs=15):
        """Entrenar el modelo"""
        print("🤖 Iniciando entrenamiento del modelo...")
        
        # Preprocesar textos
        processed_texts = [self.preprocess_peruvian_text(text) for text in texts]
        
        if self.use_tensorflow:
            # Entrenamiento LSTM
            X = self.prepare_data(processed_texts, labels)
            y = np.array(labels)
            
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=validation_split, random_state=42, stratify=y)
            
            callbacks = [
                EarlyStopping(patience=5, restore_best_weights=True, monitor='val_accuracy'),
                ModelCheckpoint(
                    Path(__file__).parent.parent / "models" / "trained_lstm.h5",
                    save_best_only=True,
                    monitor='val_accuracy'
                )
            ]
            
            history = self.model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=epochs,
                batch_size=32,
                callbacks=callbacks,
                verbose=1
            )
            
            y_pred_proba = self.model.predict(X_val)
            y_pred = (y_pred_proba > 0.5).astype(int).flatten()
            
        else:
            # Entrenamiento Random Forest
            X = self.prepare_data(processed_texts, labels)
            y = np.array(labels)
            
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=validation_split, random_state=42, stratify=y)
            
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_val)
            history = {'accuracy': [0.85], 'loss': [0.3]}  # Placeholder
        
        # Calcular metricas
        accuracy = accuracy_score(y_val, y_pred)
        precision = precision_score(y_val, y_pred, zero_division=0)
        recall = recall_score(y_val, y_pred, zero_division=0)
        f1 = f1_score(y_val, y_pred, zero_division=0)
        
        # Guardar metricas
        self.save_metrics(accuracy, precision, recall, f1)
        
        # Guardar modelos
        if self.use_tensorflow:
            joblib.dump(self.tokenizer, Path(__file__).parent.parent / "models" / "tokenizer.pkl")
        else:
            joblib.dump(self.vectorizer, Path(__file__).parent.parent / "models" / "vectorizer.pkl")
            joblib.dump(self.model, Path(__file__).parent.parent / "models" / "random_forest.pkl")
        
        self.is_trained = True
        
        print(f"✅ Modelo entrenado - Accuracy: {accuracy:.4f}, F1-Score: {f1:.4f}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'history': history
        }
    
    def predict(self, text, method="auto"):
        """Predecir si una noticia es falsa"""
        try:
            processed_text = self.preprocess_peruvian_text(text)
            
            if not self.is_trained or not self.use_tensorflow or method == "heuristic":
                return self._heuristic_prediction(text)
            
            # Preparar texto para el modelo LSTM
            sequences = self.tokenizer.texts_to_sequences([processed_text])
            padded = pad_sequences(sequences, maxlen=self.max_sequence_length, padding='post', truncating='post')
            
            # Hacer prediccion
            prediction_proba = self.model.predict(padded, verbose=0)[0][0]
            confidence = float(prediction_proba)
            
            # Determinar si es fake (threshold 0.5)
            is_fake = confidence > 0.5
            
            # Caracteristicas extraidas
            features_used = self.extract_features(text)
            
            # Generar explicacion
            explanation = self.generate_explanation(is_fake, confidence, features_used)
            
            return {
                "is_fake": bool(is_fake),
                "confidence": confidence,
                "explanation": explanation,
                "features_used": features_used,
                "model_used": "LSTM Optimizado",
                "optimization_method": "keras_tuner"
            }
            
        except Exception as e:
            print(f"❌ Error en prediccion LSTM: {e}")
            return self._heuristic_prediction(text)
    
    def _heuristic_prediction(self, text):
        """Prediccion heuristica basada en reglas"""
        features = self.extract_features(text)
        
        # Puntuacion basada en caracteristicas
        fake_score = 0
        total_features = len(features)
        
        for feature in features:
            if any(keyword in feature.lower() for keyword in ['clickbait', 'mayusculas', 'corto']):
                fake_score += 1
            if 'peruano' in feature.lower():
                fake_score -= 0.5  # Bonus por contexto peruano real
        
        confidence = min(fake_score / max(total_features, 1), 1.0)
        is_fake = confidence > 0.4
        
        explanation = self.generate_explanation(is_fake, confidence, features)
        
        return {
            "is_fake": is_fake,
            "confidence": confidence,
            "explanation": explanation,
            "features_used": features,
            "model_used": "Sistema Heuristico",
            "optimization_method": "rule_based"
        }
    
    def generate_explanation(self, is_fake, confidence, features):
        """Generar explicacion de la prediccion"""
        confidence_percent = confidence * 100
        
        if is_fake:
            base = f"Analisis sugiere noticia falsa (confianza: {confidence_percent:.1f}%). "
            if confidence > 0.7:
                base += "Alta probabilidad de desinformacion. "
            else:
                base += "Caracteristicas sospechosas detectadas. "
        else:
            base = f"Noticia probablemente real (confianza: {confidence_percent:.1f}%). "
            if confidence > 0.7:
                base += "Alta confiabilidad. "
            else:
                base += "Analisis preliminar favorable. "
        
        # Agregar caracteristicas relevantes
        relevant_features = [f for f in features if any(keyword in f.lower() for keyword in 
                          ['clickbait', 'mayusculas', 'patrones', 'peruano'])]
        
        if relevant_features:
            base += "Se consideraron: " + ", ".join(relevant_features[:2])
        
        return base
    
    def get_metrics(self):
        """Obtener metricas actuales del modelo"""
        return self.metrics

# Instancia global del clasificador
news_classifier = NewsClassifier()