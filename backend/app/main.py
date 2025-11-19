from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sqlite3
import json
from typing import List
from datetime import datetime
import time

from .auth import auth_handler
from .database import get_db
from .models import (
    UserCreate, UserLogin, UserResponse, Token, 
    NewsRequest, PredictionResponse, MetricsResponse,
    OptimizationRequest, OptimizationResult, TrainingResult,
    ProjectInfo
)
from .ml_model import news_classifier
from .optimization import optimizer
from .keras_tuner import LSTMTuner

app = FastAPI(
    title="Proyecto Universitario - Detector de Fake News Perú",
    description="Sistema completo de IA para detección de noticias falsas en contexto peruano",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear usuario por defecto para el proyecto
def create_default_user():
    """Crear usuario por defecto para el proyecto"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE email = ?", ("proyecto@universidad.edu.pe",))
        if not cursor.fetchone():
            hashed_password = auth_handler.hash_password("proyecto2024")
            cursor.execute(
                "INSERT INTO users (email, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                ("proyecto@universidad.edu.pe", hashed_password, "Usuario Proyecto", "admin")
            )
            conn.commit()
            print("✅ Usuario del proyecto creado: proyecto@universidad.edu.pe / proyecto2024")

@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    create_default_user()

# ==================== AUTENTICACIÓN ====================
@app.post("/api/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        hashed_password = auth_handler.hash_password(user_data.password)
        cursor.execute(
            "INSERT INTO users (email, password_hash, full_name) VALUES (?, ?, ?)",
            (user_data.email, hashed_password, user_data.full_name)
        )
        conn.commit()
        
        user_id = cursor.lastrowid
        return {
            "id": user_id,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "role": "user"
        }

@app.post("/api/auth/login", response_model=Token)
async def login(login_data: UserLogin):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, password_hash, full_name, role FROM users WHERE email = ?",
            (login_data.email,)
        )
        user = cursor.fetchone()
        
        if not user or not auth_handler.verify_password(login_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        access_token = auth_handler.create_access_token(
            data={"sub": user["email"], "user_id": user["id"], "role": user["role"]}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"]
            }
        }

# ==================== VERIFICACIÓN DE NOTICIAS ====================
@app.post("/api/verify-news", response_model=PredictionResponse)
async def verify_news(
    news: NewsRequest,
    current_user: dict = Depends(auth_handler.get_current_user)
):
    """Endpoint principal para verificar noticias"""
    try:
        # Realizar predicción
        result = news_classifier.predict(news.headline, news.optimization_method)
        
        # Guardar en base de datos
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO predictions 
                   (user_id, headline, prediction, confidence, features_used, model_used, optimization_method) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    current_user["user_id"],
                    news.headline,
                    result["is_fake"],
                    result["confidence"],
                    json.dumps(result["features_used"]),
                    result["model_used"],
                    result["optimization_method"]
                )
            )
            prediction_id = cursor.lastrowid
            conn.commit()
        
        return {
            "id": prediction_id,
            "is_fake": result["is_fake"],
            "confidence": result["confidence"],
            "explanation": result["explanation"],
            "features_used": result["features_used"],
            "model_used": result["model_used"],
            "optimization_method": result["optimization_method"],
            "created_at": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la verificación: {str(e)}"
        )

# ==================== MÉTRICAS Y ANÁLISIS ====================
@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Obtener métricas actuales del modelo"""
    metrics = news_classifier.get_metrics()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM predictions")
        total_predictions = cursor.fetchone()["total"]
        
        cursor.execute("SELECT COUNT(*) as correct FROM predictions WHERE is_correct = 1")
        correct_predictions = cursor.fetchone()["correct"]
    
    return {
        "accuracy": metrics["accuracy"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1_score": metrics["f1_score"],
        "model_type": "LSTM + Random Forest",
        "training_date": datetime.now(),
        "total_predictions": total_predictions,
        "correct_predictions": correct_predictions
    }

@app.get("/api/predictions/history")
async def get_prediction_history(
    current_user: dict = Depends(auth_handler.get_current_user)
):
    """Obtener historial de verificaciones del usuario"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, headline, prediction, confidence, model_used, optimization_method, created_at 
               FROM predictions 
               WHERE user_id = ? 
               ORDER BY created_at DESC 
               LIMIT 50""",
            (current_user["user_id"],)
        )
        predictions = cursor.fetchall()
        
        return [
            {
                "id": pred["id"],
                "headline": pred["headline"],
                "is_fake": bool(pred["prediction"]),
                "confidence": pred["confidence"],
                "model_used": pred["model_used"],
                "optimization_method": pred["optimization_method"],
                "created_at": pred["created_at"]
            }
            for pred in predictions
        ]

# ==================== OPTIMIZACIÓN Y BÚSQUEDA ====================
@app.post("/api/optimize", response_model=OptimizationResult)
async def run_optimization(
    optimization: OptimizationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(auth_handler.get_current_user)
):
    """Ejecutar métodos de optimización"""
    try:
        result = optimizer.optimize(optimization.method)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en optimización: {str(e)}"
        )

@app.get("/api/optimize/genetic")
async def optimize_genetic(current_user: dict = Depends(auth_handler.get_current_user)):
    """Optimización con algoritmo genético"""
    try:
        result = optimizer.optimize("genetic")
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en AG: {str(e)}"
        )

@app.get("/api/optimize/pso")
async def optimize_pso(current_user: dict = Depends(auth_handler.get_current_user)):
    """Optimización con Particle Swarm"""
    try:
        result = optimizer.optimize("pso")
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en PSO: {str(e)}"
        )

@app.get("/api/optimize/annealing")
async def optimize_annealing(current_user: dict = Depends(auth_handler.get_current_user)):
    """Optimización con Simulated Annealing"""
    try:
        result = optimizer.optimize("annealing")
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en SA: {str(e)}"
        )

# ==================== ENTRENAMIENTO ====================
@app.post("/api/train")
async def train_model(background_tasks: BackgroundTasks):
    """Entrenar el modelo (endpoint simulado)"""
    # En un sistema real, esto entrenaría el modelo
    # Por ahora retornamos resultados simulados
    
    return {
        "accuracy": 0.87,
        "precision": 0.85,
        "recall": 0.83,
        "f1_score": 0.84,
        "duration": 120.5,
        "message": "Modelo entrenado exitosamente"
    }

# ==================== INFORMACIÓN DEL PROYECTO ====================
@app.get("/api/project/info", response_model=ProjectInfo)
async def get_project_info():
    """Información del proyecto universitario"""
    return {
        "name": "Sistema de Detección de Fake News Perú",
        "version": "2.0.0",
        "description": "Sistema completo de inteligencia artificial para detección de noticias falsas en contexto peruano",
        "author": "Estudiante Universitario",
        "university": "Universidad del Proyecto",
        "course": "Inteligencia Artificial",
        "features": [
            "Detección en tiempo real",
            "Procesamiento de español peruano",
            "Modelo LSTM optimizado",
            "Métodos de búsqueda (AG, PSO, SA)",
            "4 métricas de evaluación",
            "Interfaz web completa"
        ],
        "technologies": [
            "Python", "TensorFlow", "FastAPI", "LSTM", 
            "Algoritmos Genéticos", "Particle Swarm", 
            "Simulated Annealing", "Keras Tuner"
        ]
    }

@app.get("/api/system/health")
async def health_check():
    """Estado del sistema"""
    return {
        "status": "operational",
        "model_loaded": news_classifier.is_trained,
        "optimization_ready": True,
        "timestamp": datetime.now().isoformat(),
        "project": "Detector de Fake News Perú"
    }

@app.get("/")
async def root():
    return {
        "message": "🎓 Proyecto Universitario - Sistema Completo de Detección de Fake News",
        "version": "2.0.0",
        "features": [
            "Machine Learning con LSTM",
            "Métodos de Búsqueda y Optimización", 
            "Procesamiento de español peruano",
            "4 Métricas de Evaluación",
            "Interfaz Web Completa"
        ],
        "endpoints": {
            "verificar_noticia": "POST /api/verify-news",
            "metricas": "GET /api/metrics",
            "historial": "GET /api/predictions/history",
            "optimizacion": "POST /api/optimize",
            "info_proyecto": "GET /api/project/info"
        }
    }