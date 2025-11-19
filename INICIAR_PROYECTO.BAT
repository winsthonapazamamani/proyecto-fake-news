@echo off
chcp 65001 >nul
title 🎓 PROYECTO FAKE NEWS PERÚ - SISTEMA COMPLETO

echo ====================================================
echo     PROYECTO UNIVERSITARIO - DETECTOR DE NOTICIAS FALSAS
echo     Machine Learning + Métodos de Busqueda
echo ====================================================
echo.

set PROJECT_PATH=%~dp0
set BACKEND_PATH=%PROJECT_PATH%backend
set PYTHON_PATH=%PROJECT_PATH%portable-python\python.exe

echo 🎓 Iniciando Proyecto Completo de IA...
echo.

REM Verificar Python
if not exist "%PYTHON_PATH%" (
    echo 🔍 Buscando Python en el sistema...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python no encontrado en el sistema.
        echo 🛑 El proyecto requiere Python 3.8 o superior
        pause
        exit /b 1
    )
    set PYTHON_PATH=python
)

echo ✅ Python configurado correctamente
echo.

REM Actualizar pip primero
echo 📦 Actualizando pip...
"%PYTHON_PATH%" -m pip install --upgrade pip

REM Instalar dependencias una por una para evitar conflictos
echo 📦 Instalando sistema completo de IA...
echo 🔧 Instalando dependencias basicas...
"%PYTHON_PATH%" -m pip install fastapi==0.100.0
"%PYTHON_PATH%" -m pip install uvicorn==0.23.0
"%PYTHON_PATH%" -m pip install python-multipart==0.0.6
"%PYTHON_PATH%" -m pip install python-jose[cryptography]==3.3.0
"%PYTHON_PATH%" -m pip install passlib[bcrypt]==1.7.4

echo 🤖 Instalando dependencias de Machine Learning...
"%PYTHON_PATH%" -m pip install numpy==1.24.3
"%PYTHON_PATH%" -m pip install scikit-learn==1.3.0
"%PYTHON_PATH%" -m pip install pandas==1.5.3
"%PYTHON_PATH%" -m pip install joblib==1.3.2
"%PYTHON_PATH%" -m pip install nltk==3.8.1

echo 🧠 Instalando TensorFlow y Keras...
"%PYTHON_PATH%" -m pip install tensorflow==2.12.0
"%PYTHON_PATH%" -m pip install keras-tuner==1.3.5

echo 📊 Instalando dependencias de visualizacion...
"%PYTHON_PATH%" -m pip install matplotlib==3.7.1
"%PYTHON_PATH%" -m pip install seaborn==0.12.2
"%PYTHON_PATH%" -m pip install threadpoolctl==3.2.0

echo.
echo 🗃️ Inicializando base de datos del proyecto...
"%PYTHON_PATH%" "%BACKEND_PATH%\init_database.py"

echo.
echo 🤖 Configurando modelos de Machine Learning...

REM Crear script temporal para verificar modelos
echo import sys > "%TEMP%\check_models.py"
echo sys.path.append(r"%BACKEND_PATH%") >> "%TEMP%\check_models.py"
echo try: >> "%TEMP%\check_models.py"
echo     from app.ml_model import NewsClassifier >> "%TEMP%\check_models.py"
echo     from app.optimization import Optimizer >> "%TEMP%\check_models.py"
echo     classifier = NewsClassifier() >> "%TEMP%\check_models.py"
echo     optimizer = Optimizer() >> "%TEMP%\check_models.py"
echo     print('✅ Sistema de IA listo:') >> "%TEMP%\check_models.py"
echo     print('   - Modelo LSTM cargado') >> "%TEMP%\check_models.py"
echo     print('   - Metodos de busqueda activos') >> "%TEMP%\check_models.py"
echo     print('   - Procesamiento peruano configurado') >> "%TEMP%\check_models.py"
echo except Exception as e: >> "%TEMP%\check_models.py"
echo     print('⚠️  Error cargando modelos:', str(e)) >> "%TEMP%\check_models.py"
echo     print('🔧 Entrenando modelo automaticamente...') >> "%TEMP%\check_models.py"
echo     import subprocess >> "%TEMP%\check_models.py"
echo     subprocess.run([r'%PYTHON_PATH%', r'%BACKEND_PATH%\train_model.py']) >> "%TEMP%\check_models.py"

"%PYTHON_PATH%" "%TEMP%\check_models.py"

echo.
echo 🚀 Iniciando servidores del proyecto...
echo 📍 Interfaz Web: http://localhost:8080
echo 🔧 API Backend: http://localhost:8000
echo 📊 Dashboard: http://localhost:8080
echo.

start "Backend Proyecto" "%PYTHON_PATH%" "%BACKEND_PATH%\main.py"
timeout /t 8 /nobreak >nul
start "Frontend Proyecto" "%PYTHON_PATH%" "%BACKEND_PATH%\simple_server.py"
timeout /t 4 /nobreak >nul

echo 🌐 Abriendo interfaz del proyecto...
start "" "http://localhost:8080"

echo.
echo ====================================================
echo        🎓 PROYECTO INICIADO CORRECTAMENTE
echo ====================================================
echo.
echo 🎯 CARACTERISTICAS ACTIVAS:
echo    ✅ Machine Learning (LSTM + Random Forest)
echo    ✅ Metodos de Busqueda (Genetico, PSO, Annealing)
echo    ✅ 4 Metricas (Accuracy, Precision, Recall, F1)
echo    ✅ Keras Tuner para optimizacion
echo    ✅ Procesamiento de espanol peruano
echo    ✅ Interfaz web completa
echo.
echo 📋 USO RAPIDO:
echo    1. Web: http://localhost:8080
echo    2. Usuario: proyecto@universidad.edu.pe
echo    3. Contrasena: proyecto2024
echo    4. Ver noticias en tiempo real
echo.
echo ⚠️  No cerrar esta ventana
echo.

REM Limpiar archivo temporal
del "%TEMP%\check_models.py" >nul 2>&1

pause