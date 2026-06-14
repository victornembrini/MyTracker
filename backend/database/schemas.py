from pydantic import BaseModel, Field
from datetime import date
from typing import Literal


# --- UTILISATEUR ---
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=18)
    body_weight: float = Field(..., gt=0, description="Poids corporel en kg")
    height: float = Field(..., gt=0, description="Taille en centimètres")
    birthdate: date


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    user_id: int
    model_config = {"from_attributes": True}


# --- CATALOGUE : EXERCICES ---
class ExerciceBase(BaseModel):
    nom: str
    type: Literal["barre", "haltere", "poids_corps"]


class ExerciceCreate(ExerciceBase):
    pass


class ExerciceResponse(ExerciceBase):
    exercice_id: int
    model_config = {"from_attributes": True}


# --- PLANIFICATION : SÉANCE ---
class SeancePlanifieeBase(BaseModel):
    nom: str = Field(..., max_length=10)
    split_id: int


class SeancePlanifieeCreate(SeancePlanifieeBase):
    pass


class SeancePlanifieeResponse(SeancePlanifieeBase):
    seance_plan_id: int
    model_config = {"from_attributes": True}


# --- HISTORIQUE : SÉRIES ---
class SetRealiseBase(BaseModel):
    exercice_id: int
    numero_serie: int = Field(..., gt=0)
    reps: int = Field(..., ge=0)
    charge: float = Field(..., ge=0)
    rir: int = Field(..., ge=0, le=10)


class SetRealiseCreate(SetRealiseBase):
    workout_id: int


class SetRealiseResponse(SetRealiseBase):
    set_id: int
    workout_id: int
    model_config = {"from_attributes": True}
