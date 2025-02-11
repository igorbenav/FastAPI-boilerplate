from fastcrud import FastCRUD

from ..db.token_blacklist import TokenBlacklist
from ..schemas import TokenBlacklistCreate, TokenBlacklistUpdate

CRUDTokenBlacklist = FastCRUD[TokenBlacklist, TokenBlacklistCreate, TokenBlacklistUpdate, TokenBlacklistUpdate, None, None]
crud_token_blacklist = CRUDTokenBlacklist(TokenBlacklist)
