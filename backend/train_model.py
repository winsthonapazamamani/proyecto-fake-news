import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Agregar el directorio backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.ml_model import NewsClassifier
from app.keras_tuner import LSTMTuner
from sklearn.model_selection import train_test_split

def load_or_create_dataset():
    """Cargar dataset existente o crear uno de ejemplo peruano"""
    data_path = backend_path / "data" / "peruvian_news_dataset.csv"
    
    if data_path.exists():
        print("📊 Cargando dataset peruano existente...")
        df = pd.read_csv(data_path)
    else:
        print("🔧 Creando dataset peruano de ejemplo...")
        # Dataset de ejemplo con noticias peruanas reales y falsas
        data = {
            'headline': [
                # Noticias reales peruanas (label: 0)
                "Presidente anuncia nuevas medidas económicas para reactivar el país",
                "Ministerio de Educación implementa nuevo currículo escolar nacional",
                "Exportaciones peruanas crecieron 15% en el último trimestre",
                "Gobierno inaugura nuevo hospital en región Lima",
                "PBI del Perú muestra crecimiento sostenido por sexto mes consecutivo",
                "Municipalidad de Lima anuncia plan de reforestación urbana",
                "Sunat supera meta de recaudación tributaria para este año",
                "Perú firma acuerdo comercial con nueva nación asiática",
                "Universidades peruanas mejoran en ranking internacional educativo",
                "Ministerio de Salud reporta disminución en casos de dengue",
                "BCRP mantiene tasa de interés referencial en 4.5%",
                "Minedu anuncia aumento de presupuesto para educación pública",
                "Perú logra récord en exportación de aguacate hass",
                "Gobierno lanza programa de vivienda social para familias",
                "Producción de cobre crece 12% en minas peruanas",
                
                # Noticias falsas peruanas (label: 1)
                "¡URGENTE! Descubren cura milagrosa para el cáncer en hierbas amazónicas",
                "Gobierno anuncia que desde mañana la gasolina será GRATIS",
                "SHOCKER: Presidente revela que es extraterrestre en conferencia secreta",
                "¡INCREÍBLE! Banco Central regalará dinero a todos los peruanos esta semana",
                "ALERTA: Terremoto de 9.0 grados predicted para Lima esta noche",
                "SECRETO OCULTO: Descubren ciudad perdida de los incas bajo Miraflores",
                "¡IMPACTANTE! Conoce el alimento que quita 10 años de edad al instante",
                "ATENCIÓN: Nuevo impuesto obligará a pagar por respirar aire puro",
                "¡BOMBAZO! Famoso actor peruano revelado como agente secreto ruso",
                "DESCUBREN que beber chicha morada cura instantáneamente el COVID",
                "¡EXCLUSIVO! Sunat anuncia que no habrá que pagar impuestos este año",
                "Minedu elimina todas las tareas escolares a nivel nacional",
                "Gobierno regalará casas a todos los peruanos que las soliciten",
                "Descubren que comer ceviche diario hace inmortal a las personas",
                "¡SORPRESA! Anuncian que el metro de Lima será totalmente gratuito"
            ],
            'label': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        }
        
        df = pd.DataFrame(data)
        
        # Crear directorio si no existe
        data_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(data_path, index=False)
        print("✅ Dataset peruano creado y guardado")
    
    return df

def main():
    """Función principal de entrenamiento"""
    print("="*70)
    print("           ENTRENAMIENTO DEL SISTEMA - FAKE NEWS PERÚ")
    print("           LSTM + Keras Tuner + 4 Métricas")
    print("="*70)
    
    # Cargar datos
    df = load_or_create_dataset()
    print(f"📊 Dataset cargado: {len(df)} muestras peruanas")
    print(f"   Noticias reales: {len(df[df['label'] == 0])}")
    print(f"   Noticias falsas: {len(df[df['label'] == 1])}")
    
    # Inicializar clasificador
    classifier = NewsClassifier()
    
    # Preparar datos
    texts = df['headline'].tolist()
    labels = df['label'].tolist()
    
    # Preprocesar textos
    processed_texts = [classifier.preprocess_peruvian_text(text) for text in texts]
    
    # Preparar datos para LSTM
    X = classifier.prepare_data(processed_texts, labels)
    y = np.array(labels)
    
    # Dividir datos
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"📈 División de datos:")
    print(f"   Entrenamiento: {len(X_train)} muestras")
    print(f"   Validación: {len(X_val)} muestras")
    
    # Usar Keras Tuner para optimización
    print("\n🎯 Iniciando optimización con Keras Tuner...")
    tuner = LSTMTuner()
    
    # Optimizar hiperparámetros
    best_hps = tuner.tune_model(X_train, y_train, X_val, y_val, max_trials=10)
    
    # Entrenar mejor modelo
    best_model, metrics = tuner.train_best_model(X_train, y_train, X_val, y_val, epochs=20)
    
    # Reemplazar modelo del clasificador
    classifier.model = best_model
    classifier.is_trained = True
    
    # Mostrar resultados finales
    print("\n" + "="*60)
    print("         RESULTADOS FINALES DEL ENTRENAMIENTO")
    print("="*60)
    print(f"🎯 Accuracy:  {metrics['accuracy']:.4f}")
    print(f"📊 Precision: {metrics['precision']:.4f}")
    print(f"🔍 Recall:    {metrics['recall']:.4f}")
    print(f"⭐ F1-Score:  {metrics['f1_score']:.4f}")
    print("="*60)
    
    # Probar el modelo con ejemplos peruanos
    print("\n🧪 Probando el modelo con noticias peruanas...")
    test_examples = [
        "Gobierno anuncia nuevo programa social para familias vulnerables",
        "¡INCREÍBLE! Descubren que la maca cura la diabetes instantáneamente",
        "Ministerio de Economía reporta crecimiento del PBI en 4.8%",
        "¡URGENTE! Revelan que el pisco rejuvenece 20 años"
    ]
    
    for example in test_examples:
        prediction = classifier.predict(example)
        status = "❌ FALSA" if prediction['is_fake'] else "✅ REAL"
        print(f"📰 '{example}'")
        print(f"   → Resultado: {status} (confianza: {prediction['confidence']:.2f})")
        print(f"   → Modelo: {prediction['model_used']}")
        print()

if __name__ == "__main__":
    main()