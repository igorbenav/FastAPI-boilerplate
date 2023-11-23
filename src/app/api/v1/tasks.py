from arq.jobs import Job as ArqJob
from fastapi import APIRouter, Depends

from app.core.utils import queue
from app.schemas.job import Job
from app.api.dependencies import rate_limiter

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/task", response_model=Job, status_code=201, dependencies=[Depends(rate_limiter)])
async def create_task(message: str):
    job = await queue.pool.enqueue_job("sample_background_task", message)
    return {"id": job.job_id}


@router.get("/task/{task_id}")
async def get_task(task_id: str):
    job = ArqJob(task_id, queue.pool)
    return await job.info()
