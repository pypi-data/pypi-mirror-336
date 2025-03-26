from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entity.SerializeableContent import SerializeableClass, SerializeableContent


class DatasetSourceType(Enum):
    ManualUpload = 0
    SFTPAutoload = 1
    ClientAutoload = 2
    APIUpload = 3


class ParsedMetadata(SerializeableContent):
    Parameters: bool = False
    Tracks: bool = False
    TrackCount: int = False
    TrackViewerTypes: List[str] = []


@dataclass
class DatasetSource(SerializeableClass):
    id: Optional[int] = None
    type: Optional[DatasetSourceType] = None
    name: Optional[str] = None


class ViewableEntityTypes(Enum):
    ELN = "ELN"
    CustomField = "CustomField"
