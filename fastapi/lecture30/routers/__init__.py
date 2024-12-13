from .users import router as users_router
from .items import router as items_router

# for typing-checking purpose, we are adding the below line(it is optional)
__all__ = ['items_router', 'users_router']