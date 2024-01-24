from fastcrud import FastCRUD

from ..models.tier import Tier
from ..schemas.tier import TierCreateInternal, TierDelete, TierUpdate, TierUpdateInternal

CRUDTier = FastCRUD[Tier, TierCreateInternal, TierUpdate, TierUpdateInternal, TierDelete]
crud_tiers = CRUDTier(Tier)
