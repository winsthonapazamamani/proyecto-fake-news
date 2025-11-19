# Detector de Noticias Falsas con LSTM

## Instalación
1. Clona el repositorio
2. Instala dependencias: `pip install -r requirements.txt`
3. Coloca tu dataset en `data/raw/dataset.csv`

## Uso
- Entrenar modelo: `python train_model.py`
- Probar modelo: `python test_model.py`

## Formato del Dataset
El archivo CSV debe contener:
- `text`: Contenido de la noticia
- `label`: 0 (falsa) o 1 (verdadera)