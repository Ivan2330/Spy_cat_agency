from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.models import Mission, Target
from app.schemas import MissionCreate, MissionResponse, MissionUpdate

router = APIRouter()

@router.post("/missions/", response_model=MissionResponse)
async def create_mission(mission: MissionCreate, db: AsyncSession = Depends(get_async_session)):
    db_mission = Mission(cat_id=mission.cat_id)
    db.add(db_mission)
    await db.flush()

    for target_data in mission.targets:
        db_target = Target(
            mission_id=db_mission.id,
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes,
            is_complete=target_data.is_complete
        )
        db.add(db_target)

    await db.commit()

    result = await db.execute(
        select(Mission)
        .options(selectinload(Mission.targets))
        .filter_by(id=db_mission.id)
    )
    db_mission = result.scalar_one()

    return db_mission

@router.get("/missions/{mission_id}", response_model=MissionResponse)
async def get_mission(mission_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(Mission)
        .options(selectinload(Mission.targets))
        .filter(Mission.id == mission_id)
    )
    db_mission = result.scalar_one_or_none()

    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    return db_mission

@router.put("/missions/{mission_id}", response_model=MissionResponse)
async def update_mission(mission_id: int, mission: MissionUpdate, db: AsyncSession = Depends(get_async_session)):
    db_mission = await get_mission(mission_id=mission_id, db=db)
    if db_mission and not db_mission.is_complete:
        db_mission.is_complete = mission.is_complete
        await db.commit()
        await db.refresh(db_mission)
    else:
        raise HTTPException(status_code=404, detail="Mission not found or already complete")
    return db_mission

@router.delete("/missions/{mission_id}")
async def delete_mission(mission_id: int, db: AsyncSession = Depends(get_async_session)):
    db_mission = await get_mission(mission_id=mission_id, db=db)
    if db_mission and db_mission.cat_id is None:
        await db.delete(db_mission)
        await db.commit()
        return {"detail": "Mission deleted"}
    else:
        raise HTTPException(status_code=400, detail="Mission cannot be deleted")

@router.post("/missions/{mission_id}/assign/{cat_id}", response_model=MissionResponse)
async def assign_cat_to_mission(mission_id: int, cat_id: int, db: AsyncSession = Depends(get_async_session)):
    existing_mission = await db.execute(select(Mission).filter(Mission.cat_id == cat_id, Mission.is_complete == False))
    if existing_mission.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Cat already has an active mission")

    db_mission = await get_mission(mission_id=mission_id, db=db)
    if db_mission and db_mission.cat_id is None:
        db_mission.cat_id = cat_id
        await db.commit()
        await db.refresh(db_mission)
    else:
        raise HTTPException(status_code=404, detail="Mission not found or already assigned")
    return db_mission
