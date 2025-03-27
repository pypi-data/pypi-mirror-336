from fastapi import APIRouter
from dependency_injector.wiring import inject

from api.utils.subscribe import auto_subscribe
from entrypoints_base.storage_rest_api.fileapi.storage_handler_v2 import StorageHandlerV2
from entrypoints_base.storage_rest_api.api.router.deps import StrogHandlerV2Dep

router = APIRouter()


@router.get("/files/v2")
@auto_subscribe(to_list=False)
@inject
async def get_files(page: int = None, strg_handler_v2: StorageHandlerV2 = StrogHandlerV2Dep):
    return strg_handler_v2.list_files_in_repository(page)
