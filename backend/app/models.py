from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class NewsRequest(BaseModel):
    headline: str
    content: Optional[str] = None
    optimization_method: Optional[str] = "auto"

class PredictionResponse(BaseModel):
    id: int
    is_fake: bool
    confidence: float
    explanation: str
    features_used: List[str]
    model_used: str
    optimization_method: str
    created_at: datetime

class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    model_type: str
    training_date: datetime
    total_predictions: int
    correct_predictions: int

class OptimizationRequest(BaseModel):
    method: str = "genetic"
    population_size: int = 30
    generations: int = 50

class OptimizationResult(BaseModel):
    method: str
    best_score: float
    best_params: Dict[str, Any]
    duration: float
    iterations: int

class TrainingResult(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    history: Dict[str, List[float]]
    duration: float

class ProjectInfo(BaseModel):
    name: str
    version: str
    description: str
    author: str
    university: str
    course: str
    features: List[str]
    technologies: List[str]