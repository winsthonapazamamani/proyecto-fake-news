import nltk
import ssl

def download_nltk_resources():
    """Descargar todos los recursos necesarios de NLTK"""
    
    # Solucionar problemas de SSL si es necesario
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    resources = [
        'stopwords',
        'punkt',
        'punkt_tab',
        'wordnet',
        'averaged_perceptron_tagger'
    ]
    
    print("Descargando recursos de NLTK...")
    
    for resource in resources:
        try:
            print(f"Descargando {resource}...")
            nltk.download(resource, quiet=False)
            print(f"✓ {resource} descargado correctamente")
        except Exception as e:
            print(f"✗ Error descargando {resource}: {e}")
    
    print("\nVerificando recursos descargados...")
    
    # Verificar stopwords
    try:
        from nltk.corpus import stopwords
        print(f"✓ Stopwords disponibles: {len(stopwords.words('english'))} en inglés")
        if 'spanish' in stopwords.fileids():
            print(f"✓ Stopwords disponibles: {len(stopwords.words('spanish'))} en español")
    except:
        print("✗ Stopwords no disponibles")
    
    # Verificar tokenización
    try:
        from nltk.tokenize import word_tokenize
        test_text = "Hello world this is a test"
        tokens = word_tokenize(test_text)
        print(f"✓ Tokenización funcionando: {tokens}")
    except Exception as e:
        print(f"✗ Tokenización no funciona: {e}")

if __name__ == "__main__":
    download_nltk_resources()