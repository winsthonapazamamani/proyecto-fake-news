import sys
import os

sys.path.append('src')

from peru_predictor import PeruNewsPredictor

def main():
    # Configuración
    MODEL_PATH = "models/trained_models/fake_news_model.h5"
    TOKENIZER_PATH = "models/trained_models/tokenizer.pkl"
    
    # Verificar que los archivos existan
    if not os.path.exists(MODEL_PATH):
        print("❌ Modelo no encontrado. Ejecuta train_model.py primero.")
        return
    
    if not os.path.exists(TOKENIZER_PATH):
        print("❌ Tokenizer no encontrado. Ejecuta train_model.py primero.")
        return
    
    # Cargar predictor
    print("🇵🇪 Cargando predictor de noticias peruanas...")
    predictor = PeruNewsPredictor(MODEL_PATH, TOKENIZER_PATH)
    
    # Noticias de ejemplo con contexto peruano
    test_news = [
        # Noticia probablemente verdadera
        "El Presidente del Consejo de Ministros, Alberto Otárola, anunció hoy nuevas medidas económicas para reactivar el sector construcción en Lima y provincias, según informó el Ministerio de Economía.",
        
        # Noticia probablemente falsa
        "Dina Boluarte renunció a la presidencia esta mañana tras masivas protestas en todo el país que dejaron 50 muertos, según fuentes no oficiales del Congreso.",
        
        # Noticia con patrones sospechosos
        "Terremoto de 8.5 grados sacude Lima: edificios colapsados y miles de muertos. Gobierno decreta toque de queda indefinido.",
        
        # Noticia económica falsa
        "El dólar llegará a 10 soles la próxima semana según analistas internacionales, generando pánico en los mercados locales.",
        
        # Noticia política real
        "El Congreso de la República aprobó la ley de reforma electoral con 85 votos a favor, modificando el sistema de elecciones para las próximas municipales."
    ]
    
    print("\n" + "="*80)
    print("🔍 ANALIZADOR DE NOTICIAS PERUANAS")
    print("="*80)
    
    for i, news in enumerate(test_news, 1):
        print(f"\n📰 NOTICIA {i}:")
        print(f"   {news}")
        
        resultado = predictor.predict_news(news)
        
        print(f"\n   📊 RESULTADO: {resultado['prediccion']}")
        print(f"   🎯 CONFIANZA: {resultado['confianza']:.2%}")
        print(f"   💡 EXPLICACIÓN: {resultado['explicacion']}")
        
        # Mostrar análisis detallado
        if resultado['analisis_contexto']['mentioned_politicians']:
            print(f"   👥 POLÍTICOS MENCIONADOS: {', '.join(resultado['analisis_contexto']['mentioned_politicians'])}")
        
        if resultado['analisis_contexto']['fake_patterns_detected']:
            print(f"   ⚠ PATRONES DETECTADOS: {len(resultado['analisis_contexto']['fake_patterns_detected'])}")
        
        print("-" * 80)

def interactive_mode():
    """Modo interactivo para probar noticias"""
    MODEL_PATH = "models/trained_models/fake_news_model.h5"
    TOKENIZER_PATH = "models/trained_models/tokenizer.pkl"
    
    if not os.path.exists(MODEL_PATH) or not os.path.exists(TOKENIZER_PATH):
        print("Primero entrena el modelo ejecutando: python train_model.py")
        return
    
    predictor = PeruNewsPredictor(MODEL_PATH, TOKENIZER_PATH)
    
    print("\n" + "🇵🇪" * 20)
    print("   ANALIZADOR INTERACTIVO DE NOTICIAS PERUANAS")
    print("🇵🇪" * 20)
    print("\nEscribe una noticia peruana y te diré si es falsa o verdadera.")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        noticia = input("📝 Ingresa la noticia: ").strip()
        
        if noticia.lower() in ['salir', 'exit', 'quit']:
            break
        
        if not noticia:
            continue
        
        resultado = predictor.predict_news(noticia)
        
        print(f"\n🎯 RESULTADO: {resultado['prediccion']}")
        print(f"📈 CONFIANZA: {resultado['confianza']:.2%}")
        print(f"💡 {resultado['explicacion']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
    
    # Descomenta la siguiente línea para modo interactivo
    # interactive_mode()