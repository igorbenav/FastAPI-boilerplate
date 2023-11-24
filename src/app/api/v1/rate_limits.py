from typing import Annotated

from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import fastapi

from app.api.dependencies import get_current_superuser
from app.api.paginated import PaginatedListResponse, paginated_response, compute_offset
from app.core.db.database import async_get_db
from app.core.exceptions.http_exceptions import NotFoundException, DuplicateValueException, RateLimitException
from app.crud.crud_rate_limit import crud_rate_limits
from app.crud.crud_tier import crud_tiers
from app.schemas.rate_limit import (
    RateLimitRead,
    RateLimitCreate,
    RateLimitCreateInternal,
    RateLimitUpdate
)

router = fastapi.APIRouter(tags=["rate_limits"])

@router.post("/tier/{tier_name}/rate_limit", dependencies=[Depends(get_current_superuser)], status_code=201)
async def write_rate_limit(
    request: Request, 
    tier_name: str,
    rate_limit: RateLimitCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise NotFoundException("Tier not found")

    rate_limit_internal_dict = rate_limit.model_dump()
    rate_limit_internal_dict["tier_id"] = db_tier["id"]

    db_rate_limit = await crud_rate_limits.exists(db=db, name=rate_limit_internal_dict["name"])
    if db_rate_limit:
        raise DuplicateValueException("Rate Limit Name not available")
    
    rate_limit_internal = RateLimitCreateInternal(**rate_limit_internal_dict)
    return await crud_rate_limits.create(db=db, object=rate_limit_internal)


@router.get("/tier/{tier_name}/rate_limits", response_model=PaginatedListResponse[RateLimitRead])
async def read_rate_limits(
    request: Request,
    tier_name: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10
):
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise NotFoundException("Tier not found")

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
        raise NotFoundException("Tier not found")
    
    db_rate_limit = await crud_rate_limits.get(
        db=db, 
        schema_to_select=RateLimitRead, 
        tier_id=db_tier["id"],
        id=id
    )
    if db_rate_limit is None:
        raise NotFoundException("Rate Limit not found")

    return db_rate_limit


@router.patch("/tier/{tier_name}/rate_limit/{id}", dependencies=[Depends(get_current_superuser)])
async def patch_rate_limit(
    request: Request,
    tier_name: str,
    id: int,
    values: RateLimitUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if db_tier is None:
        raise NotFoundException("Tier not found")
    
    db_rate_limit = await crud_rate_limits.get(
        db=db,
        schema_to_select=RateLimitRead, 
        tier_id=db_tier["id"],
        id=id
    )
    if db_rate_limit is None:
        raise NotFoundException("Rate Limit not found")
    
    db_rate_limit_path = await crud_rate_limits.exists(
        db=db,
        tier_id=db_tier["id"],
        path=values.path
    )
    if db_rate_limit_path is not None:
        raise DuplicateValueException("There is already a rate limit for this path")

    db_rate_limit_name = await crud_rate_limits.exists(db=db)
    if db_rate_limit_path is not None:
        raise DuplicateValueException("There is already a rate limit with this name")

    await crud_rate_limits.update(db=db, object=values, id=db_rate_limit["id"])
    return {"message": "Rate Limit updated"}


@router.delete("/tier/{tier_name}/rate_limit/{id}", dependencies=[Depends(get_current_superuser)])
async def erase_rate_limit(
    request: Request,
    tier_name: str,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)]
):
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise NotFoundException("Tier not found")
    
    db_rate_limit = await crud_rate_limits.get(
        db=db, 
        schema_to_select=RateLimitRead, 
        tier_id=db_tier["id"],
        id=id
    )
    if db_rate_limit is None:
        raise RateLimitException("Rate Limit not found")
    
    await crud_rate_limits.delete(db=db, db_row=db_rate_limit, id=db_rate_limit["id"])
    return {"message": "Rate Limit deleted"}
