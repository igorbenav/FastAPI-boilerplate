from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException, RateLimitException
from ...crud.crud_rate_limit import crud_rate_limits
from ...crud.crud_tier import crud_tiers
from ...schemas.rate_limit import RateLimitCreate, RateLimitCreateInternal, RateLimitRead, RateLimitUpdate

router = APIRouter(tags=["rate_limits"])


@router.post("/tier/{tier_name}/rate_limit", dependencies=[Depends(get_current_superuser)], status_code=201)
async def write_rate_limit(
    request: Request, tier_name: str, rate_limit: RateLimitCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> RateLimitRead:
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise NotFoundException("Tier not found")

    rate_limit_internal_dict = rate_limit.model_dump()
    rate_limit_internal_dict["tier_id"] = db_tier["id"]

    db_rate_limit = await crud_rate_limits.exists(db=db, name=rate_limit_internal_dict["name"])
    if db_rate_limit:
        raise DuplicateValueException("Rate Limit Name not available")

    rate_limit_internal = RateLimitCreateInternal(**rate_limit_internal_dict)
    created_rate_limit: RateLimitRead = await crud_rate_limits.create(db=db, object=rate_limit_internal)
    return created_rate_limit


@router.get("/tier/{tier_name}/rate_limits", response_model=PaginatedListResponse[RateLimitRead])
async def read_rate_limits(
    request: Request,
    tier_name: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise NotFoundException("Tier not found")

    rate_limits_data = await crud_rate_limits.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=RateLimitRead,
        tier_id=db_tier["id"],
    )

    response: dict[str, Any] = paginated_response(crud_data=rate_limits_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/tier/{tier_name}/rate_limit/{id}", response_model=RateLimitRead)
async def read_rate_limit(
    request: Request, tier_name: str, id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict:
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise NotFoundException("Tier not found")

    db_rate_limit: dict | None = await crud_rate_limits.get(
        db=db, schema_to_select=RateLimitRead, tier_id=db_tier["id"], id=id
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
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if db_tier is None:
        raise NotFoundException("Tier not found")

    db_rate_limit = await crud_rate_limits.get(db=db, schema_to_select=RateLimitRead, tier_id=db_tier["id"], id=id)
    if db_rate_limit is None:
        raise NotFoundException("Rate Limit not found")

    db_rate_limit_path = await crud_rate_limits.exists(db=db, tier_id=db_tier["id"], path=values.path)
    if db_rate_limit_path is not None:
        raise DuplicateValueException("There is already a rate limit for this path")

    await crud_rate_limits.exists(db=db)
    if db_rate_limit_path is not None:
        raise DuplicateValueException("There is already a rate limit with this name")

    await crud_rate_limits.update(db=db, object=values, id=db_rate_limit["id"])
    return {"message": "Rate Limit updated"}


@router.delete("/tier/{tier_name}/rate_limit/{id}", dependencies=[Depends(get_current_superuser)])
async def erase_rate_limit(
    request: Request, tier_name: str, id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_tier = await crud_tiers.get(db=db, name=tier_name)
    if not db_tier:
        raise NotFoundException("Tier not found")

    db_rate_limit = await crud_rate_limits.get(db=db, schema_to_select=RateLimitRead, tier_id=db_tier["id"], id=id)
    if db_rate_limit is None:
        raise RateLimitException("Rate Limit not found")

    await crud_rate_limits.delete(db=db, id=db_rate_limit["id"])
    return {"message": "Rate Limit deleted"}
