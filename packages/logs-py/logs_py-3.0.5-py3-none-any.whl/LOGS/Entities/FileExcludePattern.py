from typing import Optional

from LOGS.Entity.SerializeableContent import SerializeableClass


class FileExcludePattern(SerializeableClass):
    name: Optional[str] = None
    regex: Optional[str] = None
