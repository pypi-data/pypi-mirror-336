from fastapi import APIRouter

from api.routers import root
from entrypoints_base.storage_rest_api.api.router import s3_routes
from entrypoints.reactive_web.src.todo import task_query_controller

router = APIRouter()

router.include_router(root.router)
router.include_router(s3_routes.router)
router.include_router(task_query_controller.router)
