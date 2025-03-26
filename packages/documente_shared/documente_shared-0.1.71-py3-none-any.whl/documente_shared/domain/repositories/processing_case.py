from abc import ABC, abstractmethod
from typing import Optional, List

from documente_shared.domain.entities.processing_case import ProcessingCase
from documente_shared.domain.enums.common import ProcessingStatus


class ProcessingCaseRepository(ABC):

    @abstractmethod
    def find(self, case_id: str) -> Optional[ProcessingCase]:
        raise NotImplementedError

    @abstractmethod
    def persist(self, instance: ProcessingCase) -> ProcessingCase:
        raise NotImplementedError

    @abstractmethod
    def remove(self, instance: ProcessingCase):
        raise NotImplementedError

    @abstractmethod
    def filter(self, statuses: List[ProcessingStatus]) -> List[ProcessingCase]:
        raise NotImplementedError
