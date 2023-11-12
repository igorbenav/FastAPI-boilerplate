from app.crud.crud_base import CRUDBase
from app.models.rate_limit import RateLimit

from app.schemas.rate_limit import (
    RateLimitCreateInternal,
    RateLimitUpdate,
    RateLimitUpdateInternal,
    RateLimitDelete
)

CRUDRateLimit = CRUDBase[RateLimit, RateLimitCreateInternal, RateLimitUpdate, RateLimitUpdateInternal, RateLimitDelete]
crud_rate_limits = CRUDRateLimit(RateLimit)
