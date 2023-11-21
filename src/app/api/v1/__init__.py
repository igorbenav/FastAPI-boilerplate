from fastapi import APIRouter

from app.api.v1.login import router as login_router
from app.api.v1.logout import router as logout_router
from app.api.v1.users import router as users_router
from app.api.v1.posts import router as posts_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.tiers import router as tiers_router
from app.api.v1.rate_limits import router as rate_limits_router

router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(logout_router)
router.include_router(users_router)
router.include_router(posts_router)
router.include_router(tasks_router)
router.include_router(tiers_router)
router.include_router(rate_limits_router)
