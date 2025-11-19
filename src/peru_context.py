import re
import pandas as pd

class PeruContextEnhancer:
    def __init__(self):
        self.peru_keywords = {
            'instituciones': [
                'congreso', 'presidente', 'ministerio', 'pcm', 'premier', 'ministro',
                'poder judicial', 'tjpu', 'superintendencia', 'sunat', 'osiptel',
                'osiner', 'osinerg', 'indecopi', 'reniec', 'onpe', 'jne', 'tribunal',
                'municipalidad', 'gobierno regional', 'region', 'minedu', 'minsa',
                'mininter', 'minjus', 'rree', 'produce', 'agricultura'
            ],
            'partidos_politicos': [
                'fuerza popular', 'peru libre', 'accion popular', 'alianza para el progreso',
                'podemos peru', 'somos peru', 'avanza pais', 'juntos por el peru',
                'renovacion popular', 'partido morado', 'frente amplio', 'solidaridad nacional',
                'apra', 'partido nacionalista', 'victoria nacional'
            ],
            'politicos': [
                'dina boluarte', 'pedro castillo', 'martin vizcarra', 'ppk', 'alan garcia',
                'keiko fujimori', 'alberto fujimori', 'ollanta humala', 'alejandro toledo',
                'cesar acuña', 'daniel urresti', 'daniel salaverry', 'manuel merino',
                'anibal torres', 'hector valer', 'ernesto araujo', 'betssy chavez'
            ],
            'localidades': [
                'lima', 'arequipa', 'cuzco', 'trujillo', 'chiclayo', 'piura', 'iquitos',
                'huancayo', 'pucallpa', 'tacna', 'ica', 'cusco', 'ayacucho', 'puno',
                'cajamarca', 'chincha', 'barranca', 'huaraz', 'tumbes', 'moquegua',
                'madre de dios', 'amazonas', 'san martin', 'ucayali', 'pasco'
            ],
            'medios_peruanos': [
                'el comercio', 'peru21', 'trome', 'ojo', 'libero', 'rpp', 'america',
                'atv', 'panamericana', 'willax', 'tv peru', 'latina', 'exitosa'
            ],
            'problemas_comunes': [
                'protestas', 'paro', 'tomas', 'corrupcion', 'coimas', 'lavado de activos',
                'colusion', 'narco', 'mineria ilegal', 'tala ilegal', 'informalidad',
                'trafico de tierras', 'contrataciones', 'obra publica', 'sobrevaloracion'
            ]
        }
        
        self.fake_news_patterns = [
            r'(muerto|fallecido|asesinado).*(dina|presidenta|boluarte)',
            r'(renuncia|renuncio).*(presidente|ministro|congresista)',
            r'(golpe de estado|autogolpe|cierre del congreso)',
            r'(dolar.*(10|15|20) soles|sol.*(5|10) dolares)',
            r'(terremoto|sismo).*(8|9|10).*escala',
            r'(toque de queda|estado de sitio|emergencia nacional)',
            r'(congelamiento de cuentas|confiscacion de bienes)',
            r'(nuevo impuesto|impuestazo|subida de impuestos)',
            r'(crisis economica|recesion|quiebra).*peru',
            r'(marchas|protestas).*(violentas|muertos|heridos)'
        ]
    
    def analyze_peru_context(self, text):
        """
        Analizar el texto en contexto peruano
        """
        text_lower = text.lower()
        analysis = {
            'peru_relevance_score': 0,
            'mentioned_institutions': [],
            'mentioned_politicians': [],
            'mentioned_locations': [],
            'fake_patterns_detected': [],
            'contains_medios_peruanos': False
        }
        
        # Verificar instituciones mencionadas
        for institution in self.peru_keywords['instituciones']:
            if institution in text_lower:
                analysis['mentioned_institutions'].append(institution)
                analysis['peru_relevance_score'] += 1
        
        # Verificar políticos mencionados
        for politician in self.peru_keywords['politicos']:
            if politician in text_lower:
                analysis['mentioned_politicians'].append(politician)
                analysis['peru_relevance_score'] += 2
        
        # Verificar localidades
        for location in self.peru_keywords['localidades']:
            if location in text_lower:
                analysis['mentioned_locations'].append(location)
                analysis['peru_relevance_score'] += 1
        
        # Verificar medios peruanos
        for medio in self.peru_keywords['medios_peruanos']:
            if medio in text_lower:
                analysis['contains_medios_peruanos'] = True
                analysis['peru_relevance_score'] += 1
        
        # Detectar patrones de fake news
        for pattern in self.fake_news_patterns:
            if re.search(pattern, text_lower):
                analysis['fake_patterns_detected'].append(pattern)
                analysis['peru_relevance_score'] += 3
        
        return analysis
    
    def enhance_features(self, text, base_prediction, confidence):
        """
        Mejorar la predicción con contexto peruano
        """
        analysis = self.analyze_peru_context(text)
        
        # Ajustar confianza basado en análisis de contexto
        confidence_adjustment = 0
        
        # Si detecta patrones de fake news, aumentar probabilidad de ser falso
        if analysis['fake_patterns_detected']:
            confidence_adjustment += 0.2 * len(analysis['fake_patterns_detected'])
        
        # Si menciona medios peruanos, ligeramente más confiable
        if analysis['contains_medios_peruanos']:
            confidence_adjustment -= 0.1
        
        # Ajustar confianza final
        final_confidence = min(0.95, max(0.05, confidence + confidence_adjustment))
        
        # Determinar predicción final
        final_prediction = "FALSA" if base_prediction == 0 else "VERDADERA"
        
        # Si hay muchos patrones de fake news, forzar predicción a falsa
        if len(analysis['fake_patterns_detected']) >= 2:
            final_prediction = "FALSA"
            final_confidence = max(final_confidence, 0.7)
        
        return {
            'prediccion': final_prediction,
            'confianza': final_confidence,
            'analisis_contexto': analysis,
            'explicacion': self.generate_explanation(final_prediction, analysis)
        }
    
    def generate_explanation(self, prediction, analysis):
        """
        Generar explicación basada en el análisis de contexto
        """
        explanations = []
        
        if prediction == "FALSA":
            if analysis['fake_patterns_detected']:
                explanations.append("❌ Contiene patrones típicos de noticias falsas peruanas")
            if analysis['mentioned_politicians']:
                explanations.append(f"⚠ Menciona figuras políticas: {', '.join(analysis['mentioned_politicians'])}")
        else:
            if analysis['contains_medios_peruanos']:
                explanations.append("✅ Se mencionan medios de comunicación peruanos")
            if analysis['mentioned_institutions']:
                explanations.append("📋 Incluye referencias a instituciones oficiales")
        
        if analysis['peru_relevance_score'] > 5:
            explanations.append("🇵🇪 Alto contenido de contexto peruano")
        
        return " | ".join(explanations) if explanations else "Análisis estándar aplicado"