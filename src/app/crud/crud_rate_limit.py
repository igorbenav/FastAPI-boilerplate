from .crud_base import CRUDBase
from ..models.rate_limit import RateLimit

from ..schemas.rate_limit import (
    RateLimitCreateInternal,
    RateLimitUpdate,
    RateLimitUpdateInternal,
    RateLimitDelete
)

CRUDRateLimit = CRUDBase[RateLimit, RateLimitCreateInternal, RateLimitUpdate, RateLimitUpdateInternal, RateLimitDelete]
crud_rate_limits = CRUDRateLimit(RateLimit)
