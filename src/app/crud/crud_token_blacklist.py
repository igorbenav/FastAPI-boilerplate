from app.crud.crud_base import CRUDBase
from app.models.token_blacklist import TokenBlacklist
from app.schemas.token_blacklist import TokenBlacklistCreate, TokenBlacklistUpdate

CRUDTokenBlacklist = CRUDBase[TokenBlacklist, TokenBlacklistCreate, TokenBlacklistUpdate, TokenBlacklistUpdate, None]
crud_token_blacklist = CRUDTokenBlacklist(TokenBlacklist)
