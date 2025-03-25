import qiclib.packages.grpc.datatypes_pb2 as _datatypes_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConverterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADC: _ClassVar[ConverterType]
    DAC: _ClassVar[ConverterType]
ADC: ConverterType
DAC: ConverterType

class ConverterIndex(_message.Message):
    __slots__ = ("type", "index")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    type: ConverterType
    index: int
    def __init__(self, type: _Optional[_Union[ConverterType, str]] = ..., index: _Optional[int] = ...) -> None: ...

class IndexedDouble(_message.Message):
    __slots__ = ("index", "value")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    index: ConverterIndex
    value: float
    def __init__(self, index: _Optional[_Union[ConverterIndex, _Mapping]] = ..., value: _Optional[float] = ...) -> None: ...

class RfDcIndex(_message.Message):
    __slots__ = ("tile", "block")
    TILE_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    tile: int
    block: int
    def __init__(self, tile: _Optional[int] = ..., block: _Optional[int] = ...) -> None: ...
