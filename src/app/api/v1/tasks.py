from arq.jobs import Job as ArqJob
from fastapi import APIRouter, HTTPException

from app.core import queue
from app.schemas.job import Job

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/task", response_model=Job, status_code=201)
async def create_task(message: str):
    job = await queue.pool.enqueue_job("sample_background_task", message)
    return {"id": job.job_id}


@router.get("/task/{task_id}")
async def get_task(task_id: str):
    job = ArqJob(task_id, queue.pool)
    return await job.info()
