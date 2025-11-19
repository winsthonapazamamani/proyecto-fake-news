import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout, SpatialDropout1D, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os

class ModelTrainer:
    def __init__(self, max_features, max_len, embedding_dim=100):
        self.max_features = max_features
        self.max_len = max_len
        self.embedding_dim = embedding_dim
        self.model = None
        self.history = None
    
    def build_model(self):
        """
        Construir modelo LSTM
        """
        self.model = Sequential([
            Embedding(self.max_features, self.embedding_dim, input_length=self.max_len),
            SpatialDropout1D(0.3),
            Bidirectional(LSTM(64, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)),
            Bidirectional(LSTM(32, dropout=0.2, recurrent_dropout=0.2)),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(32, activation='relu'),
            Dropout(0.3),
            Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            loss='binary_crossentropy',
            optimizer='adam',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        print("Modelo construido:")
        print(self.model.summary())
        return self.model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=20, batch_size=32):
        """
        Entrenar el modelo
        """
        # Callbacks
        callbacks = [
            EarlyStopping(patience=5, restore_best_weights=True),
            ModelCheckpoint(
                'models/trained_models/best_model.h5',
                save_best_only=True,
                monitor='val_accuracy',
                mode='max'
            )
        ]
        
        self.history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_val, y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        return self.history
    
    def evaluate_model(self, X_test, y_test):
        """
        Evaluar el modelo
        """
        if self.model is None:
            print("Error: Modelo no entrenado")
            return
        
        # Predicciones
        y_pred_proba = self.model.predict(X_test)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        
        # Métricas
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Exactitud (Accuracy): {accuracy:.4f}")
        print("\nReporte de Clasificación:")
        print(classification_report(y_test, y_pred, target_names=['Falsa', 'Verdadera']))
        
        return y_pred, y_pred_proba
    
    def plot_training_history(self, save_path=None):
        """
        Graficar historial de entrenamiento
        """
        if self.history is None:
            print("Error: No hay historial de entrenamiento")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Precisión
        ax1.plot(self.history.history['accuracy'], label='Entrenamiento')
        ax1.plot(self.history.history['val_accuracy'], label='Validación')
        ax1.set_title('Precisión del Modelo')
        ax1.set_xlabel('Época')
        ax1.set_ylabel('Precisión')
        ax1.legend()
        
        # Pérdida
        ax2.plot(self.history.history['loss'], label='Entrenamiento')
        ax2.plot(self.history.history['val_loss'], label='Validación')
        ax2.set_title('Pérdida del Modelo')
        ax2.set_xlabel('Época')
        ax2.set_ylabel('Pérdida')
        ax2.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_confusion_matrix(self, y_true, y_pred, save_path=None):
        """
        Graficar matriz de confusión
        """
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Falsa', 'Verdadera'],
                    yticklabels=['Falsa', 'Verdadera'])
        plt.title('Matriz de Confusión')
        plt.ylabel('Etiqueta Real')
        plt.xlabel('Etiqueta Predicha')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_model(self, filepath):
        """
        Guardar modelo entrenado
        """
        if self.model is None:
            print("Error: No hay modelo para guardar")
            return
        
        self.model.save(filepath)
        print(f"Modelo guardado en: {filepath}")