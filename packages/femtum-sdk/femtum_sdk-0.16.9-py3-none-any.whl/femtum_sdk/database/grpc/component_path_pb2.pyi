from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ComponentPath(_message.Message):
    __slots__ = ("Wafer", "Reticle", "Die", "Circuit")
    WAFER_FIELD_NUMBER: _ClassVar[int]
    RETICLE_FIELD_NUMBER: _ClassVar[int]
    DIE_FIELD_NUMBER: _ClassVar[int]
    CIRCUIT_FIELD_NUMBER: _ClassVar[int]
    Wafer: str
    Reticle: str
    Die: str
    Circuit: str
    def __init__(self, Wafer: _Optional[str] = ..., Reticle: _Optional[str] = ..., Die: _Optional[str] = ..., Circuit: _Optional[str] = ...) -> None: ...
