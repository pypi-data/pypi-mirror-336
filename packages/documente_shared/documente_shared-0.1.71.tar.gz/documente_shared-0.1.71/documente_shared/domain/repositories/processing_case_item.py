from abc import ABC, abstractmethod
from typing import Optional, List

from documente_shared.domain.entities.processing_case import ProcessingCase
from documente_shared.domain.entities.processing_case_item import ProcessingCaseItem
from documente_shared.domain.enums.common import ProcessingStatus


class ProcessingCaseItemRepository(ABC):

    @abstractmethod
    def find(self, digest: str) -> Optional[ProcessingCaseItem]:
        raise NotImplementedError

    @abstractmethod
    def persist(self, instance: ProcessingCaseItem) -> ProcessingCaseItem:
        raise NotImplementedError

    @abstractmethod
    def remove(self, instance: ProcessingCaseItem):
        raise NotImplementedError

    @abstractmethod
    def filter(self, statuses: List[ProcessingStatus]) -> List[ProcessingCase]:
        raise NotImplementedError

    @abstractmethod
    def filter_by_case_id(self, case_id: str) -> List[ProcessingCase]:
        raise NotImplementedError
