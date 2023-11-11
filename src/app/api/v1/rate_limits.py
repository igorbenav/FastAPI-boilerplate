from typing import Annotated

from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import fastapi

from app.schemas.rate_limit import (
    RateLimitRead,
    RateLimitCreate,
    RateLimitCreateInternal,
    RateLimitUpdate
)
from app.api.dependencies import get_current_superuser
from app.core.database import async_get_db
from app.crud.crud_rate_limit import crud_rate_limits
from app.crud.crud_tier import crud_tiers
from app.api.paginated import PaginatedListResponse, paginated_response, compute_offset

router = fastapi.APIRouter(tags=["rate_limits"])

@router.post("/tier/{name}/rate_limit", dependencies=[Depends(get_current_superuser)], status_code=201)
async def write_rate_limit(
    request: Request, 
    name: str,
    rate_limit: RateLimitCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_tier = await crud_tiers.get(db=db, name=name)
    if not db_tier:
        raise HTTPException(status_code=404, detail="Tier not found")

    rate_limit_internal_dict = rate_limit.model_dump()
    rate_limit_internal_dict["tier_id"] = db_tier["id"]

    db_rate_limit = await crud_rate_limits.exists(db=db, name=rate_limit_internal_dict["name"])
    if db_rate_limit:
        raise HTTPException(status_code=400, detail="Rate Limit Name not available")
    
    rate_limit_internal = RateLimitCreateInternal(**rate_limit_internal_dict)
    return await crud_rate_limits.create(db=db, object=rate_limit_internal)


@router.get("/tier/{name}/rate_limits", response_model=PaginatedListResponse[RateLimitRead])
async def read_rate_limits(
    request: Request,
    name: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10
):
    db_tier = await crud_tiers.get(db=db, name=name)
    if not db_tier:
        raise HTTPException(status_code=404, detail="Tier not found")

    rate_limits_data = await crud_rate_limits.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=RateLimitRead,
        tier_id=db_tier["id"]
    )

    return paginated_response(
        crud_data=rate_limits_data, 
        page=page, 
        items_per_page=items_per_page
    )


@router.get("/tier/{tier_name}/rate_limit/{id}", response_model=RateLimitRead)
async def read_rate_limit(
    request: Request,
    tier_name: str,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    
    db_rate_limit = await crud_rate_limits.get(
        db=db, 
        schema_to_select=RateLimitRead, 
        tier_id=db_tier["id"],
        id=id
    )
    if db_rate_limit is None:
        raise HTTPException(status_code=404, detail="Rate Limit not found")

    return db_rate_limit


@router.patch("/tier/{tier_name}/rate_limit/{path}", dependencies=[Depends(get_current_superuser)])
async def patch_rate_limit(
    request: Request,
    tier_name: str,
    id: int,
    values: RateLimitUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    
    db_rate_limit = await crud_rate_limits.get(
        db=db, 
        schema_to_select=RateLimitRead, 
        tier_id=db_tier["id"],
        id=id
    )
    if db_rate_limit is None:
        raise HTTPException(status_code=404, detail="Rate Limit not found")
    
    await crud_rate_limits.update(db=db, object=values, id=db_rate_limit["id"])
    return {"message": "Rate Limit updated"}


@router.delete("/tier/{tier_name}/rate_limit/{path}", dependencies=[Depends(get_current_superuser)])
async def erase_rate_limit(
    request: Request,
    tier_name: str,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise HTTPException(status_code=404, detail="Tier not found")
    
    db_rate_limit = await crud_rate_limits.get(
        db=db, 
        schema_to_select=RateLimitRead, 
        tier_id=db_tier["id"],
        id=id
    )
    if db_rate_limit is None:
        raise HTTPException(status_code=404, detail="Rate Limit not found")
    
    await crud_rate_limits.delete(db=db, db_row=db_rate_limit, id=db_rate_limit["id"])
    return {"message": "Rate Limit deleted"}
