import re
import pandas as pd
import numpy as np
from datetime import datetime

class EconomicNewsDetector:
    def __init__(self):
        # Datos económicos reales de Perú (para comparación)
        self.real_economic_indicators = {
            'dolar': {'min': 3.6, 'max': 3.9, 'current': 3.75},
            'inflacion': {'min': 2.0, 'max': 4.0, 'current': 2.8},
            'crecimiento_pib': {'min': -1.0, 'max': 6.0, 'current': 2.5},
            'tasa_interes': {'min': 5.0, 'max': 7.5, 'current': 6.25},
            'reservas_internacionales': {'min': 60000, 'max': 80000, 'current': 72000},
            'deuda_publica': {'min': 30, 'max': 35, 'current': 32.5}
        }
        
        # Patrones de noticias económicas falsas comunes
        self.economic_fake_patterns = [
            # Patrones de dólar exagerado
            r'dólar.*(1[0-9]|[5-9])[.,]\d*\s*soles',
            r'sol.*(1[0-9]|[5-9])[.,]\d*\s*dólares',
            r'tipo de cambio.*(1[0-9]|[5-9])[.,]\d*',
            
            # Patrones de inflación exagerada
            r'inflación.*(1[0-9]|[5-9])\d*\%',
            r'precios.*(1[0-9]|[5-9])\d*\%',
            r'IPC.*(1[0-9]|[5-9])\d*\%',
            
            # Patrones de crisis económica
            r'recesión.*\d+\s*meses',
            r'quiebra.*\d+\s*empresas',
            r'desempleo.*(1[0-9]|[5-9])\d*\%',
            
            # Patrones de números imposibles
            r'crecimiento.*(-?\d{2,})[.,]\d*\%',  # Crecimiento > 10% o < -10%
            r'PIB.*(-?\d{2,})[.,]\d*\%',
            
            # Patrones de medidas extremas
            r'nuevo impuesto.*\d+\%',
            r'devaluación.*\d+\%',
            r'congelamiento.*cuentas',
            r'corralito.*bancario'
        ]
        
        # Instituciones económicas oficiales
        self.official_economic_institutions = [
            'bcrp', 'banco central', 'mef', 'ministerio de economía',
            'inei', 'instituto nacional de estadística',
            'sbs', 'superintendencia de banca',
            'sunat', 'superintendencia nacional de aduanas',
            'bvl', 'bolsa de valores de lima',
            'fmi', 'fondomonetario', 'banco mundial'
        ]
        
        # Economistas y autoridades reconocidas
        self.recognized_economists = [
            'julio velarde', 'presidente bcrp', 'alex contreras', 'ministro economía',
            'diana rosas', 'adrian armas', 'humberto speziani', 'roque benavides',
            'carlos anderson', 'wálter bayly', 'german lara'
        ]

    def extract_economic_data(self, text):
        """
        Extraer datos económicos mencionados en el texto
        """
        text_lower = text.lower()
        extracted_data = {}
        
        # Extraer menciones de dólar
        dollar_matches = re.findall(r'dólar.*?(\d+[.,]\d+)\s*soles?', text_lower)
        if dollar_matches:
            extracted_data['dolar'] = float(dollar_matches[0].replace(',', '.'))
        
        # Extraer inflación
        inflation_matches = re.findall(r'inflación.*?(\d+[.,]\d+)%', text_lower)
        if inflation_matches:
            extracted_data['inflacion'] = float(inflation_matches[0].replace(',', '.'))
        
        # Extraer crecimiento PIB
        pib_matches = re.findall(r'(?:crecimiento|PIB).*?(-?\d+[.,]\d+)%', text_lower)
        if pib_matches:
            extracted_data['crecimiento_pib'] = float(pib_matches[0].replace(',', '.'))
        
        # Extraer tasas de interés
        interest_matches = re.findall(r'tasa.*?interés.*?(\d+[.,]\d+)%', text_lower)
        if interest_matches:
            extracted_data['tasa_interes'] = float(interest_matches[0].replace(',', '.'))
        
        return extracted_data

    def analyze_economic_credibility(self, text):
        """
        Analizar credibilidad de noticia económica
        """
        analysis = {
            'is_economic_news': False,
            'economic_indicators_mentioned': [],
            'data_anomalies': [],
            'institutional_support': False,
            'expert_mentions': False,
            'fake_patterns_detected': [],
            'credibility_score': 0.5,  # Neutral por defecto
            'economic_analysis': ''
        }
        
        text_lower = text.lower()
        
        # Verificar si es noticia económica
        economic_keywords = [
            'dólar', 'sol', 'tipo de cambio', 'inflación', 'precios', 'IPC',
            'PIB', 'crecimiento', 'recesión', 'economía', 'mercado', 'bolsa',
            'impuesto', 'tasa', 'interés', 'reservas', 'deuda', 'déficit'
        ]
        
        economic_mentions = [kw for kw in economic_keywords if kw in text_lower]
        if len(economic_mentions) >= 2:
            analysis['is_economic_news'] = True
            analysis['economic_indicators_mentioned'] = economic_mentions
        
        # Extraer datos económicos
        extracted_data = self.extract_economic_data(text)
        
        # Verificar anomalías en datos
        for indicator, value in extracted_data.items():
            if indicator in self.real_economic_indicators:
                real_range = self.real_economic_indicators[indicator]
                if value < real_range['min'] or value > real_range['max']:
                    analysis['data_anomalies'].append(
                        f"{indicator}: {value} (fuera de rango real: {real_range['min']}-{real_range['max']})"
                    )
                    analysis['credibility_score'] -= 0.3
        
        # Verificar patrones de fake news económicas
        for pattern in self.economic_fake_patterns:
            if re.search(pattern, text_lower):
                analysis['fake_patterns_detected'].append(pattern)
                analysis['credibility_score'] -= 0.2
        
        # Verificar menciones institucionales
        for institution in self.official_economic_institutions:
            if institution in text_lower:
                analysis['institutional_support'] = True
                analysis['credibility_score'] += 0.15
                break
        
        # Verificar menciones de expertos
        for expert in self.recognized_economists:
            if expert in text_lower:
                analysis['expert_mentions'] = True
                analysis['credibility_score'] += 0.1
                break
        
        # Generar análisis económico
        analysis['economic_analysis'] = self.generate_economic_analysis(
            analysis, extracted_data, text_lower
        )
        
        return analysis

    def generate_economic_analysis(self, analysis, extracted_data, text_lower):
        """
        Generar análisis económico detallado
        """
        analysis_parts = []
        
        if analysis['data_anomalies']:
            analysis_parts.append("⚠ DATOS ECONÓMICOS SOSPECHOSOS:")
            for anomaly in analysis['data_anomalies']:
                analysis_parts.append(f"   • {anomaly}")
        
        if analysis['fake_patterns_detected']:
            analysis_parts.append("🚨 PATRONES DE NOTICIAS FALSAS:")
            for pattern in analysis['fake_patterns_detected'][:3]:
                clean_pattern = pattern.replace('.*', '...').replace(r'\d+', 'NÚMERO')
                analysis_parts.append(f"   • Patrón: {clean_pattern}")
        
        if analysis['institutional_support']:
            analysis_parts.append("✅ MENCIONA INSTITUCIONES OFICIALES")
        
        if analysis['expert_mentions']:
            analysis_parts.append("✅ INCLUYE REFERENCIAS DE EXPERTOS")
        
        # Análisis específico por tipo de noticia económica
        if 'dólar' in text_lower or 'sol' in text_lower:
            analysis_parts.append("💵 NOTICIA SOBRE TIPO DE CAMBIO:")
            if any(p in text_lower for p in ['10', '15', '20']):
                analysis_parts.append("   • Valores extremos de dólar (10+ soles) son improbables")
        
        if 'inflación' in text_lower:
            analysis_parts.append("📈 NOTICIA SOBRE INFLACIÓN:")
            analysis_parts.append("   • Inflación real Perú: 2-4% anual")
        
        if 'PIB' in text_lower or 'crecimiento' in text_lower:
            analysis_parts.append("📊 NOTICIA SOBRE CRECIMIENTO:")
            analysis_parts.append("   • Crecimiento real Perú: 2-4% anual")
        
        return "\n".join(analysis_parts) if analysis_parts else "Análisis económico estándar"

    def enhance_economic_prediction(self, base_prediction, base_confidence, text):
        """
        Mejorar predicción con análisis económico
        """
        economic_analysis = self.analyze_economic_credibility(text)
        
        if not economic_analysis['is_economic_news']:
            return {
                'prediction': base_prediction,
                'confidence': base_confidence,
                'economic_analysis': economic_analysis
            }
        
        # Ajustar basado en análisis económico
        credibility = economic_analysis['credibility_score']
        adjusted_confidence = base_confidence
        
        if credibility < 0.3:
            # Noticia económica muy sospechosa
            adjusted_prediction = "FALSA"
            adjusted_confidence = max(base_confidence, 0.7)
        elif credibility > 0.7:
            # Noticia económica creíble
            adjusted_prediction = "VERDADERA" if base_prediction == "VERDADERA" else base_prediction
            adjusted_confidence = min(base_confidence + 0.1, 0.95)
        else:
            # Mantener predicción base
            adjusted_prediction = base_prediction
            adjusted_confidence = base_confidence
        
        return {
            'prediction': adjusted_prediction,
            'confidence': adjusted_confidence,
            'economic_analysis': economic_analysis
        }