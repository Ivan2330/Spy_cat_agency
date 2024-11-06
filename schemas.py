from pydantic import BaseModel, Field
from typing import List, Optional
from app.cat_api import validate_breed


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    is_complete: bool = False

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None

class TargetResponse(TargetBase):
    id: int
    mission_id: int

    class Config:
        orm_mode = True

class CatBase(BaseModel):
    name: str
    experience_years: int = Field(..., ge=0)
    breed: str
    salary: float = Field(..., gt=0)

class CatCreate(BaseModel):
    name: str
    experience_years: int = Field(..., ge=0)
    breed: str
    salary: float = Field(..., gt=0)
    
class CatUpdate(BaseModel):
    salary: float = Field(..., gt=0)

class CatResponse(CatBase):
    id: int

    class Config:
        orm_mode = True

class MissionBase(BaseModel):
    is_complete: bool = False

class MissionCreate(MissionBase):
    cat_id: Optional[int] = None
    targets: List[TargetCreate] = Field(..., min_items=1, max_items=3)

class MissionUpdate(BaseModel):
    is_complete: Optional[bool] = None

class MissionResponse(MissionBase):
    id: int
    cat_id: Optional[int] = None
    targets: List[TargetResponse] = []

    class Config:
        orm_mode = True
