from fastapi import APIRouter
from . import catalog
from . import orders

router = APIRouter()
router.include_router(catalog.router)
router.include_router(orders.router)


