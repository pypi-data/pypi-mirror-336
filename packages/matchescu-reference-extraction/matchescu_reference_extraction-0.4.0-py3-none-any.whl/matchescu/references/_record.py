from collections.abc import Iterable

from matchescu.data import Record
from matchescu.typing import EntityReferenceIdentifier


class EntityReference(Record):
    id: EntityReferenceIdentifier

    def __init__(self, identifier: EntityReferenceIdentifier, value: Iterable):
        super().__init__(value)
        self.id = identifier

    def as_dict(self) -> dict:
        return {
            attr_name: self._attr_values[attr_idx]
            for attr_name, attr_idx in self._attr_names.items()
        }
