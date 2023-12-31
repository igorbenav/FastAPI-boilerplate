from ..models.rate_limit import RateLimit
from ..schemas.rate_limit import RateLimitCreateInternal, RateLimitDelete, RateLimitUpdate, RateLimitUpdateInternal
from .crud_base import CRUDBase

CRUDRateLimit = CRUDBase[RateLimit, RateLimitCreateInternal, RateLimitUpdate, RateLimitUpdateInternal, RateLimitDelete]
crud_rate_limits = CRUDRateLimit(RateLimit)
