from typing import Optional

from LOGS.Entities.LabNotebookEntryContent.TextAttribute import TextAttribute
from LOGS.Entity.SerializeableContent import SerializeableContent


class IEntryContentWithTextAttribute(SerializeableContent):
    _attrs: Optional[TextAttribute] = None

    @property
    def attrs(self) -> Optional[TextAttribute]:
        return self._attrs

    @attrs.setter
    def attrs(self, value):
        self._attrs = self.checkAndConvertNullable(value, TextAttribute, "attrs")
