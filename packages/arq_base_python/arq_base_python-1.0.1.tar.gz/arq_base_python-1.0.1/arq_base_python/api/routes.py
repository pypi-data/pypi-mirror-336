from fastapi import APIRouter

from arq_base_python.api.routers import root
from arq_base_python.entrypoints_base.storage_rest_api.api.router import s3_routes
# from entrypoints.reactive_web.src.todo import task_query_controller

router = APIRouter()

router.include_router(root.router)
router.include_router(s3_routes.router)
# router.include_router(task_query_controller.router)
