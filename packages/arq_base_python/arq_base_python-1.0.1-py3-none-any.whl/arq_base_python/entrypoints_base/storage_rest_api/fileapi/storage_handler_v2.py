from reactivex import Observable, of
from reactivex import operators as op
from arq_base_python.cqrs.usecases.src.storage_use_case import StorageUseCase


class StorageHandlerV2:
    PAGE_SIZE = 50

    def __init__(self, storage_use_case: StorageUseCase):
        self.storage_use_case = storage_use_case

    def list_files_in_repository(self, page: int) -> Observable[dict]:
        def get_keys(page: int):
            if page == None:
                return self.storage_use_case.list_all()
            else:
                return self.storage_use_case.list_by_page(page, self.PAGE_SIZE)

        def create_response(keys: list[str]):
            return {
                "pageSize": self.PAGE_SIZE,
                "page": page,
                "files": keys,
                "commandId": None,
                "parentId": None,
            }

        return of(page).pipe(
            op.flat_map(get_keys),
            op.to_list(),
            op.map(create_response),
        )
