import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Descargar recursos de NLTK (solo primera vez)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text):
        """Limpia y preprocesa texto"""
        if not text:
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover caracteres especiales y números
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenización
        tokens = word_tokenize(text)
        
        # Remover stopwords y stemming
        filtered_tokens = [
            self.stemmer.stem(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]
        
        return ' '.join(filtered_tokens)
    
    def preprocess_batch(self, texts):
        """Preprocesa una lista de textos"""
        return [self.clean_text(text) for text in texts]

# Instancia global para fácil acceso
preprocessor = TextPreprocessor()

# Función de conveniencia
def clean_text(text):
    return preprocessor.clean_text(text)