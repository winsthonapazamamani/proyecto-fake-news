# 🇵🇪 Clasificador de Noticias Falsas con LSTM

Este proyecto tiene como objetivo desarrollar un **sistema de clasificación de noticias falsas** utilizando **Redes Neuronales Recurrentes (LSTM)** en un contexto **peruano**, empleando titulares y contenidos de medios locales verificados.

---

## 🧠 Descripción del Proyecto

El sistema permite **detectar si una noticia es verdadera o falsa** mediante un modelo de Inteligencia Artificial entrenado con un **dataset en español de titulares peruanos**, recolectados de fuentes como **Ama Llulla, Ojo Público y medios nacionales**.

El proyecto integra:
- **Modelo de IA (LSTM)** para procesamiento de lenguaje natural (NLP).
- **API REST (FastAPI)** para consultas automáticas.
- **Interfaz Web** que permite ingresar titulares o URLs de noticias.
- **Base de datos (MySQL/PostgreSQL)** para almacenar consultas, usuarios y resultados.

---

## 🏗️ Arquitectura del Sistema
---
<img width="894" height="599" alt="image" src="https://github.com/user-attachments/assets/c5772423-7a1b-4f89-857e-2c78046b8e08" />

## 🚀 Tecnologías Utilizadas

| Componente | Tecnología |
|-------------|-------------|
| Lenguaje | Python 3.11 |
| Framework Backend | FastAPI |
| Modelo IA | LSTM (Keras / TensorFlow) |
| Preprocesamiento NLP | NLTK, SpaCy |
| Base de Datos | MySQL / PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Control de versiones | Git / GitHub |
| Despliegue | Docker, Railway / Heroku |

---

## 📂 Estructura del Repositorio

<img width="1590" height="293" alt="image" src="https://github.com/user-attachments/assets/d9285392-dd2d-4920-88c8-23a8561a4371" />

---

## ⚙️ Instalación y Uso
---

---
## 🔧 1. Clonar el repositorio
---
git clone https://github.com/usuario/ClasificadorNoticiasFalsas-LSTM-Peru.git
cd ClasificadorNoticiasFalsas-LSTM-Peru

---
## 🧠 2. Ejecutar la API
uvicorn app.main:app --reload
---
---
🌐 3. Abrir el navegador

Abre la siguiente URL en tu navegador:

🔗 http://127.0.0.1:8000/docs

Desde ahí podrás probar los endpoints:

/predict_text

/predict_url
---
---
## 📊 Dataset
---
El dataset incluye más de 5,000 titulares en español obtenidos de medios peruanos y portales de verificación.

| Columna     | Descripción                |
| ----------- | -------------------------- |
| `titulo`    | Titular de la noticia      |
| `contenido` | Texto principal (opcional) |
| `etiqueta`  | 0 = Verdadera, 1 = Falsa   |

---
## 🧩 Métricas del Modelo
---
| Métrica   | Valor |
| --------- | ----- |
| Accuracy  | 0.91  |
| Recall    | 0.87  |
| Precision | 0.89  |
| F1-score  | 0.88  |

---
