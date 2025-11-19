import pandas as pd
import numpy as np
import sys
import os
from sklearn.model_selection import train_test_split

# Agregar src al path
sys.path.append('src')

from data_preprocessing import DataPreprocessor
from model_training import ModelTrainer

def load_and_validate_dataset(csv_path):
    """
    Cargar y validar dataset CSV - VERSION CORREGIDA
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
        print(f"Columnas encontradas: {list(df.columns)}")
        
        # Crear una copia para no modificar el original
        df_processed = df.copy()
        
        # Mapear nombres de columnas
        text_column = None
        label_column = None
        
        # Buscar columna de texto
        text_candidates = ['Text', 'text', 'content', 'article', 'news', 'title', 'message']
        for col in text_candidates:
            if col in df_processed.columns:
                text_column = col
                break
        
        # Buscar columna de etiqueta
        label_candidates = ['class', 'label', 'category', 'type', 'is_fake', 'target', 'classification']
        for col in label_candidates:
            if col in df_processed.columns:
                label_column = col
                break
        
        if not text_column:
            print("Error: No se encontró columna de texto")
            return None
        
        if not label_column:
            print("Error: No se encontró columna de etiqueta")
            return None
        
        print(f"Columna de texto identificada: '{text_column}'")
        print(f"Columna de etiqueta identificada: '{label_column}'")
        
        # Renombrar columnas internamente (sin modificar el DataFrame original)
        # Usaremos los nombres originales en el procesamiento
        
        # Limpiar datos nulos usando los nombres originales
        initial_count = len(df_processed)
        df_processed = df_processed.dropna(subset=[text_column, label_column])
        final_count = len(df_processed)
        
        if initial_count != final_count:
            print(f"Se eliminaron {initial_count - final_count} filas con valores nulos")
        
        # Convertir etiquetas a numérico si es necesario
        if df_processed[label_column].dtype == 'object':
            print("Convirtiendo etiquetas a formato numérico...")
            unique_labels = df_processed[label_column].unique()
            print(f"Etiquetas únicas encontradas: {unique_labels}")
            
            # Mapear a 0 y 1
            label_mapping = {}
            for label in unique_labels:
                label_str = str(label).lower()
                if any(word in label_str for word in ['fake', 'false', '0', 'no', 'incorrect', 'wrong']):
                    label_mapping[label] = 0
                elif any(word in label_str for word in ['real', 'true', '1', 'yes', 'correct', 'accurate']):
                    label_mapping[label] = 1
                else:
                    # Por defecto, usar el orden alfabético
                    if len(label_mapping) == 0:
                        label_mapping[label] = 0
                    else:
                        label_mapping[label] = 1
            
            df_processed[label_column] = df_processed[label_column].map(label_mapping)
            print(f"Mapeo de etiquetas aplicado: {label_mapping}")
        
        # Verificar que tenemos valores numéricos
        if df_processed[label_column].isna().any():
            print("Advertencia: Algunas etiquetas no pudieron ser convertidas")
            df_processed = df_processed.dropna(subset=[label_column])
        
        # Verificar distribución
        print("\nDistribución de etiquetas:")
        label_counts = df_processed[label_column].value_counts()
        print(label_counts)
        print(f"Valores únicos en etiquetas: {df_processed[label_column].unique()}")
        
        # Devolver el DataFrame y los nombres de columnas
        return {
            'dataframe': df_processed,
            'text_column': text_column,
            'label_column': label_column
        }
    
    except Exception as e:
        print(f"Error cargando dataset: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_data_samples(data_info):
    """
    Mostrar muestras de datos para verificar
    """
    df = data_info['dataframe']
    text_col = data_info['text_column']
    label_col = data_info['label_column']
    
    print(f"\nPrimeras 5 filas del dataset:")
    print(df[[text_col, label_col]].head())
    
    print(f"\nMuestras de cada clase:")
    for label_value in sorted(df[label_col].unique()):
        samples = df[df[label_col] == label_value].head(2)
        print(f"\nClase {label_value} ({len(samples)} muestras):")
        for idx, row in samples.iterrows():
            print(f"  Texto: {row[text_col][:100]}...")
            print(f"  Etiqueta: {row[label_col]}")

def main():
    # Configuración
    CSV_PATH = "data/raw/dataset.csv"  # Asegúrate que esta ruta es correcta
    MODEL_SAVE_PATH = "models/trained_models/fake_news_model.h5"
    TOKENIZER_SAVE_PATH = "models/trained_models/tokenizer.pkl"
    
    # Crear directorios si no existen
    os.makedirs('models/trained_models', exist_ok=True)
    os.makedirs('tests/test_results', exist_ok=True)
    os.makedirs('data/raw', exist_ok=True)
    
    # Verificar que el archivo existe
    if not os.path.exists(CSV_PATH):
        print(f"Error: No se encuentra el archivo {CSV_PATH}")
        print("Asegúrate de que el dataset esté en la ubicación correcta")
        return
    
    # Cargar dataset
    print("Cargando dataset...")
    data_info = load_and_validate_dataset(CSV_PATH)
    
    if data_info is None:
        print("No se pudo cargar el dataset. Verifica la ruta y el formato.")
        return
    
    # Mostrar muestras de datos
    check_data_samples(data_info)
    
    # Preparar datos
    df = data_info['dataframe']
    text_col = data_info['text_column']
    label_col = data_info['label_column']
    
    texts = df[text_col].tolist()
    labels = df[label_col].tolist()
    
    print(f"\nTotal de textos: {len(texts)}")
    print(f"Total de etiquetas: {len(labels)}")
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    print(f"\nDivisión de datos:")
    print(f"Entrenamiento: {len(X_train)} muestras")
    print(f"Validación: {len(X_val)} muestras")
    print(f"Prueba: {len(X_test)} muestras")
    
    # Preprocesar datos
    preprocessor = DataPreprocessor(max_features=10000, max_len=200)
    
    print("\nPreprocesando datos de entrenamiento...")
    X_train_processed, y_train_processed, tokenizer = preprocessor.prepare_data(X_train, y_train)
    
    print("Preprocesando datos de validación...")
    X_val_processed, y_val_processed, _ = preprocessor.prepare_data(X_val, y_val, tokenizer=tokenizer)
    
    print("Preprocesando datos de prueba...")
    X_test_processed, y_test_processed, _ = preprocessor.prepare_data(X_test, y_test, tokenizer=tokenizer)
    
    print(f"\nForma de los datos procesados:")
    print(f"X_train: {X_train_processed.shape}")
    print(f"X_val: {X_val_processed.shape}")
    print(f"X_test: {X_test_processed.shape}")
    
    # Entrenar modelo
    trainer = ModelTrainer(
        max_features=preprocessor.max_features,
        max_len=preprocessor.max_len,
        embedding_dim=100
    )
    
    model = trainer.build_model()
    
    print("\nComenzando entrenamiento...")
    history = trainer.train(
        X_train_processed, y_train_processed,
        X_val_processed, y_val_processed,
        epochs=15,  # Reducido para prueba
        batch_size=32
    )
    
    # Evaluar modelo
    print("\nEvaluando modelo...")
    y_pred, y_pred_proba = trainer.evaluate_model(X_test_processed, y_test_processed)
    
    # Guardar modelo y tokenizer
    trainer.save_model(MODEL_SAVE_PATH)
    preprocessor.save_tokenizer(TOKENIZER_SAVE_PATH)
    
    # Visualizaciones
    trainer.plot_training_history('tests/test_results/training_history.png')
    trainer.plot_confusion_matrix(y_test_processed, y_pred, 'tests/test_results/confusion_matrix.png')
    
    # Guardar resultados de prueba
    test_results = pd.DataFrame({
        'text': X_test,
        'true_label': y_test_processed,
        'predicted_label': y_pred,
        'confidence': y_pred_proba.flatten()
    })
    test_results.to_csv('tests/test_predictions.csv', index=False)
    
    print("\nProceso completado exitosamente!")
    print(f"Modelo guardado en: {MODEL_SAVE_PATH}")
    print(f"Tokenizer guardado en: {TOKENIZER_SAVE_PATH}")

if __name__ == "__main__":
    main()