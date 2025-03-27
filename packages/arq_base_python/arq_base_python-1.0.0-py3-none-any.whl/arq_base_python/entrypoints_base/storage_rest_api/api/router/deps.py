from fastapi import Depends
from entrypoints_base.storage_rest_api.fileapi.storage_handler_v2 import StorageHandlerV2
from dependency_injector.wiring import Provide
from containers.application_container import Application


StrogHandlerV2Dep: StorageHandlerV2 = Depends(
    Provide[Application.storage_container.storage_handler_v2])
