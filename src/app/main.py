from .core.config import settings
from .api import router
from .core.setup import create_application

app = create_application(router=router, settings=settings)
