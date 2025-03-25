import qiclib.packages.grpc.datatypes_pb2 as _datatypes_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Channel(_message.Message):
    __slots__ = ("channel", "type")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ADC: _ClassVar[Channel.Type]
        DAC: _ClassVar[Channel.Type]
    ADC: Channel.Type
    DAC: Channel.Type
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    channel: int
    type: Channel.Type
    def __init__(self, channel: _Optional[int] = ..., type: _Optional[_Union[Channel.Type, str]] = ...) -> None: ...

class Number(_message.Message):
    __slots__ = ("channel", "value")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    channel: Channel
    value: int
    def __init__(self, channel: _Optional[_Union[Channel, _Mapping]] = ..., value: _Optional[int] = ...) -> None: ...

class Float(_message.Message):
    __slots__ = ("channel", "value")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    channel: Channel
    value: float
    def __init__(self, channel: _Optional[_Union[Channel, _Mapping]] = ..., value: _Optional[float] = ...) -> None: ...
