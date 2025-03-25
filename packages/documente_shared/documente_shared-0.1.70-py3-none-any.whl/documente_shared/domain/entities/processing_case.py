from dataclasses import dataclass
from datetime import datetime, tzinfo
from typing import Optional, List

from documente_shared.application.time_utils import get_datetime_from_data
from documente_shared.domain.constants import la_paz_tz
from documente_shared.domain.entities.processing_case_item import ProcessingCaseItem
from documente_shared.domain.enums.common import ProcessingStatus
from documente_shared.domain.enums.processing_case import ProcessingCaseCategory


@dataclass
class ProcessingCase(object):
    id: str
    status: ProcessingStatus
    category: Optional[ProcessingCaseCategory] = None
    enqueued_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    feedback: Optional[list | dict] = None
    completed_at: Optional[datetime] = None
    metadata: Optional[dict] = None
    items: Optional[List[ProcessingCaseItem]] = None

    def __post_init__(self):
        self.items = self.items or []

    @property
    def is_procesable(self) -> bool:
        return self.items and len(self.items) > 0

    def pending(self, timezone: tzinfo = la_paz_tz):
        self.status = ProcessingStatus.PENDING
        self.started_at = None

    def enqueue(self, timezone: tzinfo = la_paz_tz):
        self.status = ProcessingStatus.ENQUEUED
        self.enqueued_at = datetime.now(tz=timezone)

    def processing(self, timezone: tzinfo = la_paz_tz):
        self.status = ProcessingStatus.PROCESSING
        self.started_at = datetime.now(tz=timezone)

    def failed(
        self,
        error_message: Optional[str] = None,
        timezone: tzinfo = la_paz_tz,
    ):
        self.status = ProcessingStatus.FAILED
        self.failed_at = datetime.now(tz=timezone)

    def completed(self, timezone: tzinfo = la_paz_tz):
        self.status = ProcessingStatus.COMPLETED
        self.completed_at = datetime.now(tz=timezone)

    def deleted(self):
        self.status = ProcessingStatus.DELETED
    
    def __eq__(self, other: 'ProcessingCase') -> bool:
        if not other:
            return False

        return (
            self.id == other.id
            and self.status == other.status
            and self.category == other.category
            and self.enqueued_at == other.enqueued_at
            and self.started_at == other.started_at
            and self.failed_at == other.failed_at
            and self.feedback == other.feedback
            and self.completed_at == other.completed_at
            and self.metadata == other.metadata
        )

    @property
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'status': str(self.status),
            'category': (
                str(self.category)
                if self.category else None
            ),
            'enqueued_at': self.enqueued_at.isoformat() if self.enqueued_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'failed_at': self.failed_at.isoformat() if self.failed_at else None,
            'feedback': self.feedback,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'metadata': self.metadata,
            'items': [item.to_dict for item in self.items],
        }

    @property
    def to_persist_dict(self) -> dict:
        return self.to_dict

    def overload(
        self,
        new_instance: 'ProcessingCase',
        properties: List[str] = None,
    ):
        instance_properties = properties or [
            'status',
            'category',
            'enqueued_at',
            'started_at',
            'failed_at',
            'feedback',
            'completed_at',
            'metadata',
            'items',
        ]
        for _property in instance_properties:
            property_value = getattr(new_instance, _property)
            if not hasattr(self, _property):
                continue
            setattr(self, _property, property_value)
        return self

    @classmethod
    def from_dict(cls, data: dict) -> 'ProcessingCase':
        return cls(
            id=data.get('id'),
            status=ProcessingStatus.from_value(data.get('status')),
            category=(
                ProcessingCaseCategory.from_value(data.get('category'))
                if data.get('category') else None
            ),
            enqueued_at=get_datetime_from_data(input_datetime=data.get('enqueued_at')),
            started_at=get_datetime_from_data(input_datetime=data.get('started_at')),
            failed_at=get_datetime_from_data(input_datetime=data.get('failed_at')),
            feedback=data.get('feedback'),
            metadata=data.get('metadata', {}),
            completed_at=get_datetime_from_data(input_datetime=data.get('completed_at')),
            items=[
                ProcessingCaseItem.from_dict(item_dict)
                for item_dict in data.get('items', [])
            ],
        )
