from typing import Dict, Optional, Any

from arq.jobs import Job as ArqJob
from fastapi import APIRouter, Depends

from ...core.utils import queue
from ...schemas.job import Job
from ...api.dependencies import rate_limiter

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/task", response_model=Job, status_code=201, dependencies=[Depends(rate_limiter)])
async def create_task(message: str) -> Dict[str, str]:
    """
    Create a new background task.

    Parameters
    ----------
    message: str
        The message or data to be processed by the task.

    Returns
    -------
    Dict[str, str]
        A dictionary containing the ID of the created task.
    """
    job = await queue.pool.enqueue_job("sample_background_task", message)
    return {"id": job.job_id}


@router.get("/task/{task_id}")
async def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a specific background task.

    Parameters
    ----------
    task_id: str
        The ID of the task.

    Returns
    -------
    Optional[Dict[str, Any]]
        A dictionary containing information about the task if found, or None otherwise.
    """
    job = ArqJob(task_id, queue.pool)
    job_info: dict = await job.info()
    return job_info
