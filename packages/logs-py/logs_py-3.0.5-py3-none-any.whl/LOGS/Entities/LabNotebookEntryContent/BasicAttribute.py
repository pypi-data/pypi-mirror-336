from typing import Optional

from LOGS.Entity.SerializeableContent import SerializeableContent


class BasicAttribute(SerializeableContent):
    _id: Optional[str] = None

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value):
        self._id = self.checkAndConvertNullable(value, str, "id")
