import keras_tuner as kt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout, Bidirectional
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path
from .database import get_db

class LSTMTuner:
    def __init__(self, vocab_size=10000, max_sequence_length=200, embedding_dim=100):
        self.vocab_size = vocab_size
        self.max_sequence_length = max_sequence_length
        self.embedding_dim = embedding_dim
        self.best_hyperparameters = None
        
    def build_model(self, hp):
        """Construir modelo LSTM con hiperparámetros optimizables"""
        model = Sequential()
        
        # Capa de embedding
        model.add(Embedding(
            input_dim=self.vocab_size,
            output_dim=hp.Int('embedding_dim', min_value=50, max_value=200, step=50),
            input_length=self.max_sequence_length
        ))
        
        # Capas LSTM bidireccionales
        for i in range(hp.Int('num_layers', 1, 3)):
            units = hp.Int(f'units_layer_{i}', min_value=32, max_value=256, step=32)
            return_sequences = i < hp.Int('num_layers', 1, 3) - 1
            
            model.add(Bidirectional(LSTM(
                units=units,
                return_sequences=return_sequences,
                dropout=hp.Float(f'dropout_{i}', min_value=0.2, max_value=0.5, step=0.1),
                recurrent_dropout=hp.Float(f'recurrent_dropout_{i}', min_value=0.2, max_value=0.5, step=0.1)
            )))
        
        # Capas densas
        for i in range(hp.Int('num_dense_layers', 1, 3)):
            units = hp.Int(f'dense_units_{i}', min_value=16, max_value=128, step=16)
            model.add(Dense(units, activation=hp.Choice(f'dense_activation_{i}', ['relu', 'tanh'])))
            model.add(Dropout(hp.Float(f'dense_dropout_{i}', min_value=0.2, max_value=0.5, step=0.1)))
        
        # Capa de salida
        model.add(Dense(1, activation='sigmoid'))
        
        # Compilar modelo
        learning_rate = hp.Choice('learning_rate', values=[1e-4, 1e-3, 1e-2])
        optimizer_name = hp.Choice('optimizer', ['adam', 'rmsprop'])
        
        if optimizer_name == 'adam':
            optimizer = Adam(learning_rate=learning_rate)
        else:
            optimizer = RMSprop(learning_rate=learning_rate)
            
        model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def tune_model(self, X_train, y_train, X_val, y_val, max_trials=15, executions_per_trial=1):
        """Optimizar hiperparámetros usando Keras Tuner"""
        print("🎯 Iniciando Keras Tuner...")
        
        # Definir el tuner
        tuner = kt.RandomSearch(
            self.build_model,
            objective='val_accuracy',
            max_trials=max_trials,
            executions_per_trial=executions_per_trial,
            directory='tuner_results',
            project_name='news_classifier_lstm',
            overwrite=True
        )
        
        # Callback para early stopping
        stop_early = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        
        # Búsqueda de hiperparámetros
        tuner.search(
            X_train, y_train,
            epochs=20,
            validation_data=(X_val, y_val),
            callbacks=[stop_early],
            batch_size=32,
            verbose=1
        )
        
        # Obtener mejores hiperparámetros
        self.best_hyperparameters = tuner.get_best_hyperparameters(num_trials=1)[0]
        
        print("✅ Keras Tuner completado")
        print("🎯 Mejores hiperparámetros encontrados:")
        for param, value in self.best_hyperparameters.values.items():
            print(f"   {param}: {value}")
        
        return self.best_hyperparameters
    
    def train_best_model(self, X_train, y_train, X_val, y_val, epochs=25):
        """Entrenar el modelo con los mejores hiperparámetros"""
        if self.best_hyperparameters is None:
            raise ValueError("Debes ejecutar tune_model primero")
        
        print("🤖 Entrenando modelo con mejores hiperparámetros...")
        
        # Construir modelo con mejores hiperparámetros
        best_model = self.build_model(self.best_hyperparameters)
        
        # Callbacks
        callbacks = [
            EarlyStopping(patience=7, restore_best_weights=True, monitor='val_accuracy'),
            tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-7)
        ]
        
        # Entrenar modelo
        history = best_model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluar modelo
        y_pred_proba = best_model.predict(X_val)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        
        # Calcular métricas
        accuracy = accuracy_score(y_val, y_pred)
        precision = precision_score(y_val, y_pred, zero_division=0)
        recall = recall_score(y_val, y_pred, zero_division=0)
        f1 = f1_score(y_val, y_pred, zero_division=0)
        
        # Guardar hiperparámetros
        self.save_hyperparameters(accuracy)
        
        print(f"✅ Modelo entrenado - Accuracy: {accuracy:.4f}, F1-Score: {f1:.4f}")
        
        return best_model, {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'history': history.history,
            'hyperparameters': self.best_hyperparameters.values
        }
    
    def save_hyperparameters(self, best_score):
        """Guardar hiperparámetros optimizados"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO hyperparameters 
                    (units_layer1, units_layer2, learning_rate, dropout_rate, optimizer, activation, tuner_method, best_score) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        self.best_hyperparameters.get('units_layer_0', 64),
                        self.best_hyperparameters.get('units_layer_1', 32),
                        self.best_hyperparameters.get('learning_rate', 0.001),
                        self.best_hyperparameters.get('dropout_0', 0.3),
                        self.best_hyperparameters.get('optimizer', 'adam'),
                        'relu',
                        'keras_tuner',
                        best_score
                    )
                )
                conn.commit()
            
            print("✅ Hiperparámetros guardados en la base de datos")
            
        except Exception as e:
            print(f"❌ Error guardando hiperparámetros: {e}")