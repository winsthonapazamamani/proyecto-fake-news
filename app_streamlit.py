import streamlit as st
import sys
import os

sys.path.append('src')

from peru_predictor import PeruNewsPredictor

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Noticias Peruanas",
    page_icon="🇵🇪",
    layout="wide"
)

# Título principal
st.title("🇵🇪 Analizador de Noticias Peruanas")
st.markdown("### Detecta si una noticia es falsa o verdadera usando IA")

# Sidebar
st.sidebar.header("Configuración")
st.sidebar.info("""
Este sistema analiza noticias peruanas usando:
- Modelo LSTM entrenado
- Contexto político peruano
- Patrones de fake news
""")

# Verificar si el modelo existe
MODEL_PATH = "models/trained_models/fake_news_model.h5"
TOKENIZER_PATH = "models/trained_models/tokenizer.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("❌ Modelo no encontrado. Ejecuta primero: `python train_model.py`")
    st.stop()

# Cargar modelo (con cache)
@st.cache_resource
def load_predictor():
    return PeruNewsPredictor(MODEL_PATH, TOKENIZER_PATH)

predictor = load_predictor()

# Área de entrada de texto
st.header("📝 Ingresa la noticia a analizar")
news_text = st.text_area(
    "Pega la noticia aquí:",
    height=150,
    placeholder="Ejemplo: El presidente anunció nuevas medidas económicas para reactivar el sector construcción..."
)

# Botón de análisis
if st.button("🔍 Analizar Noticia", type="primary"):
    if not news_text.strip():
        st.warning("⚠ Por favor ingresa una noticia para analizar")
    else:
        with st.spinner("Analizando noticia..."):
            resultado = predictor.predict_news(news_text)
        
        # Mostrar resultados
        st.header("📊 Resultados del Análisis")
        
        # Tarjeta de resultado principal
        if resultado['prediccion'] == 'VERDADERA':
            st.success(f"✅ **NOTICIA VERDADERA** - Confianza: {resultado['confianza']:.1%}")
        else:
            st.error(f"❌ **NOTICIA FALSA** - Confianza: {resultado['confianza']:.1%}")
        
        # Explicación
        st.info(f"💡 **Explicación:** {resultado['explicacion']}")
        
        # Detalles del análisis
        st.subheader("🔍 Detalles del Análisis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Contexto Peruano:**")
            analisis = resultado['analisis_contexto']
            
            if analisis['mentioned_politicians']:
                st.write(f"👥 **Políticos:** {', '.join(analisis['mentioned_politicians'])}")
            
            if analisis['mentioned_institutions']:
                st.write(f"🏛️ **Instituciones:** {', '.join(analisis['mentioned_institutions'][:3])}")
            
            if analisis['mentioned_locations']:
                st.write(f"📍 **Ubicaciones:** {', '.join(analisis['mentioned_locations'][:3])}")
        
        with col2:
            st.write("**Indicadores:**")
            st.write(f"📊 **Relevancia Perú:** {analisis['peru_relevance_score']}/10")
            
            if analisis['contains_medios_peruanos']:
                st.write("📰 **Menciona medios peruanos**")
            
            if analisis['fake_patterns_detected']:
                st.write(f"⚠ **Patrones sospechosos:** {len(analisis['fake_patterns_detected'])}")

# Sección de ejemplos
st.header("📚 Ejemplos para Probar")
ejemplos = {
    "Noticia probablemente falsa": "Dina Boluarte renunció a la presidencia tras protestas con 50 muertos según fuentes no oficiales",
    "Noticia probablemente verdadera": "Ministerio de Economía anunció programa de reactivación para pequeñas empresas en Lima",
    "Noticia económica falsa": "Dólar llegará a 10 soles la próxima semana según analistas internacionales"
}

for titulo, ejemplo in ejemplos.items():
    if st.button(f"Probar: {titulo}"):
        st.session_state.news_text = ejemplo
        st.rerun()

# Footer
st.markdown("---")
st.markdown("*Sistema desarrollado para análisis de noticias peruanas*")
