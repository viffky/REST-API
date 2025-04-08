from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.db.models.task import Task as DBTask  
from app.schemas.task import TaskCreate, TaskUpdate, Task, TaskStatus

router = APIRouter()

@router.get("/", response_model=List[Task])
async def read_tasks(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    status: Optional[TaskStatus] = Query(None)
):
    query = select(DBTask)
    if status:
        query = query.where(DBTask.status == status)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBTask).where(DBTask.id == task_id))
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.post("/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = DBTask(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task 

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBTask).where(DBTask.id == task_id))
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)

    if 'status' in update_data:
        if db_task.status == TaskStatus.DONE and update_data['status'] != TaskStatus.DONE:
            raise HTTPException(
                status_code=400,
                detail="Cannot modify status from DONE"
            )

    for key, value in update_data.items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBTask).where(DBTask.id == task_id))
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(db_task)
    await db.commit()
