from fastapi import APIRouter
from .v1 import catalog_router

router = APIRouter()
router.include_router(catalog_router)


