from app.core.config import settings
from app.api import router
from app.core.setup import create_application

app = create_application(router=router, settings=settings)
