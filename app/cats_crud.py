from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_async_session
from app.models import Cat
from app.schemas import CatCreate, CatUpdate, CatResponse
from app.cat_api import validate_breed

router = APIRouter()

@router.post("/cats/", response_model=CatResponse)
async def create_cat(cat: CatCreate, db: AsyncSession = Depends(get_async_session)):
    await validate_breed(cat.breed)
    
    db_cat = Cat(
        name=cat.name,
        experience_years=cat.experience_years,
        breed=cat.breed,
        salary=cat.salary
    )
    db.add(db_cat)
    await db.commit()
    await db.refresh(db_cat)
    return db_cat

@router.get("/cats/{cat_id}", response_model=CatResponse)
async def get_cat(cat_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Cat).filter(Cat.id == cat_id))
    db_cat = result.scalar_one_or_none()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat

@router.get("/cats/", response_model=list[CatResponse])
async def get_cats(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Cat).offset(skip).limit(limit))
    return result.scalars().all()

@router.put("/cats/{cat_id}", response_model=CatResponse)
async def update_cat(cat_id: int, cat: CatUpdate, db: AsyncSession = Depends(get_async_session)):
    db_cat = await get_cat(cat_id=cat_id, db=db)
    if db_cat:
        db_cat.salary = cat.salary
        await db.commit()
        await db.refresh(db_cat)
    else:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat

@router.delete("/cats/{cat_id}")
async def delete_cat(cat_id: int, db: AsyncSession = Depends(get_async_session)):
    db_cat = await get_cat(cat_id=cat_id, db=db)
    if db_cat:
        await db.delete(db_cat)
        await db.commit()
        return {"detail": "Cat deleted"}
    else:
        raise HTTPException(status_code=404, detail="Cat not found")
