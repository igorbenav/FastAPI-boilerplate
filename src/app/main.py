from fastapi import FastAPI

from app.core.database import Base

from app.api import router
from app.core.database import async_engine as engine
from app.core.config import settings

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        contact=settings.CONTACT,
        license_info=settings.CONTACT
    )

    application.include_router(router)
    application.add_event_handler("startup", create_tables)

    return application


app = create_application()
