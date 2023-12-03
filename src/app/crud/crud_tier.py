from .crud_base import CRUDBase
from ..models.tier import Tier
from ..schemas.tier import (
    TierCreateInternal, 
    TierUpdate, 
    TierUpdateInternal, 
    TierDelete)

CRUDTier = CRUDBase[Tier, TierCreateInternal, TierUpdate, TierUpdateInternal, TierDelete]
crud_tiers = CRUDTier(Tier)
