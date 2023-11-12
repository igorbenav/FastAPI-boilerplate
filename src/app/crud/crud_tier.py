from app.crud.crud_base import CRUDBase
from app.models.tier import Tier
from app.schemas.tier import (
    TierCreateInternal, 
    TierUpdate, 
    TierUpdateInternal, 
    TierDelete)

CRUDTier = CRUDBase[Tier, TierCreateInternal, TierUpdate, TierUpdateInternal, TierDelete]
crud_tiers = CRUDTier(Tier)
