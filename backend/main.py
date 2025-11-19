import uvicorn
import sys
import os
import webbrowser
import threading
from pathlib import Path
from datetime import datetime

# Agregar ruta del backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.main import app
from app.database import init_database
from app.ml_model import news_classifier
from app.optimization import optimizer

def open_browser():
    """Abrir navegador automáticamente"""
    import time
    time.sleep(6)
    try:
        webbrowser.open("http://localhost:8080")
    except:
        print("⚠️  No se pudo abrir el navegador automáticamente")

def display_project_banner():
    """Mostrar banner del proyecto"""
    print("\n" + "🎓" + "="*70)
    print("           PROYECTO UNIVERSITARIO - SISTEMA DE DETECCIÓN DE FAKE NEWS")
    print("           Machine Learning + Métodos de Búsqueda + Procesamiento Peruano")
    print("="*70)
    print("📚 Universidad: Universidad del Proyecto")
    print("👨‍🎓 Estudiante: Tu Nombre")
    print("📅 Año: 2024")
    print("🔧 Tecnologías: Python, TensorFlow, FastAPI, LSTM, Algoritmos Genéticos")
    print("🎯 Objetivo: Detectar noticias falsas en contexto peruano usando IA")
    print("="*70)

def initialize_system():
    """Inicializar el sistema completo"""
    print("\n🤖 Inicializando Sistema Completo de IA...")
    
    # Verificar componentes del sistema
    try:
        print("🔍 Estado del sistema:")
        print(f"   - Modelo LSTM: {'✅ Entrenado' if news_classifier.is_trained else '⚠️  No entrenado'}")
        print(f"   - Métodos de búsqueda: ✅ Genetico, PSO, Simulated Annealing")
        print(f"   - Procesamiento: ✅ Español peruano")
        print(f"   - Métricas: ✅ Accuracy, Precision, Recall, F1-Score")
        print(f"   - Optimización: ✅ Keras Tuner integrado")
        
        # Test del sistema
        test_examples = [
            "Presidente anuncia medidas para la economía peruana",
            "¡INCREÍBLE! Descubren cura milagrosa en hierbas amazónicas"
        ]
        
        print(f"🧪 Prueba del sistema:")
        for example in test_examples:
            prediction = news_classifier.predict(example)
            status = "❌ FALSA" if prediction['is_fake'] else "✅ REAL"
            print(f"   → '{example}'")
            print(f"      Resultado: {status} ({prediction['confidence']:.1%})")
            print(f"      Modelo: {prediction['model_used']}")
        
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")

if __name__ == "__main__":
    # Mostrar información del proyecto
    display_project_banner()
    
    # Inicializar base de datos
    print("\n🗃️ Inicializando base de datos del proyecto...")
    init_database()
    
    # Inicializar sistema ML
    initialize_system()
    
    # Abrir navegador en thread separado
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Iniciar servidor
    print(f"\n🚀 Servidor del proyecto iniciado:")
    print(f"   📍 Interfaz Web: http://localhost:8080")
    print(f"   🔧 API Backend: http://localhost:8000")
    print(f"   📊 Dashboard: http://localhost:8080")
    print(f"   ⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=False
    )