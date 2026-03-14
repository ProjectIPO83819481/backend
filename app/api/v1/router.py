from fastapi import APIRouter
from . import catalog

router = APIRouter()
router.include_router(catalog.router)


