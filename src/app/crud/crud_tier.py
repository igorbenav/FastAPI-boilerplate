from ..models.tier import Tier
from ..schemas.tier import TierCreateInternal, TierDelete, TierUpdate, TierUpdateInternal
from .crud_base import CRUDBase

CRUDTier = CRUDBase[Tier, TierCreateInternal, TierUpdate, TierUpdateInternal, TierDelete]
crud_tiers = CRUDTier(Tier)
