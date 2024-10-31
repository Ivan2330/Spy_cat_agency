from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.models import Target
from app.schemas import TargetUpdate, TargetResponse

router = APIRouter()

@router.put("/missions/{mission_id}/targets/{target_id}", response_model=TargetResponse)
async def update_target(
    mission_id: int,
    target_id: int,
    target_data: TargetUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    
    result = await db.execute(
        select(Target)
        .options(selectinload(Target.mission))
        .filter(Target.id == target_id, Target.mission_id == mission_id)
    )
    db_target = result.scalar_one_or_none()

    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found or does not belong to mission")

    if target_data.notes:
        db_target.notes = target_data.notes
    if target_data.is_complete is not None:
        db_target.is_complete = target_data.is_complete

    await db.commit()
    await db.refresh(db_target)

    return db_target
