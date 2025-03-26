from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OUTPUT: _ClassVar[DataType]
    VIEW: _ClassVar[DataType]
OUTPUT: DataType
VIEW: DataType

class StorageData(_message.Message):
    __slots__ = ("data", "mission_id", "name", "timestamp", "type")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    data: _struct_pb2.Struct
    mission_id: str
    name: str
    timestamp: _timestamp_pb2.Timestamp
    type: DataType
    def __init__(self, data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., mission_id: _Optional[str] = ..., name: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., type: _Optional[_Union[DataType, str]] = ...) -> None: ...

class StoreDataRequest(_message.Message):
    __slots__ = ("data", "mission_id", "name", "type")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    data: _struct_pb2.Struct
    mission_id: str
    name: str
    type: DataType
    def __init__(self, data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., mission_id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[DataType, str]] = ...) -> None: ...

class StoreDataResponse(_message.Message):
    __slots__ = ("success", "stored_data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STORED_DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    stored_data: StorageData
    def __init__(self, success: bool = ..., stored_data: _Optional[_Union[StorageData, _Mapping]] = ...) -> None: ...

class GetDataByMissionRequest(_message.Message):
    __slots__ = ("mission_id",)
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    def __init__(self, mission_id: _Optional[str] = ...) -> None: ...

class GetDataByMissionResponse(_message.Message):
    __slots__ = ("data_items",)
    DATA_ITEMS_FIELD_NUMBER: _ClassVar[int]
    data_items: _containers.RepeatedCompositeFieldContainer[StorageData]
    def __init__(self, data_items: _Optional[_Iterable[_Union[StorageData, _Mapping]]] = ...) -> None: ...

class GetDataByNameRequest(_message.Message):
    __slots__ = ("mission_id", "name")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetDataByNameResponse(_message.Message):
    __slots__ = ("success", "stored_data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STORED_DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    stored_data: StorageData
    def __init__(self, success: bool = ..., stored_data: _Optional[_Union[StorageData, _Mapping]] = ...) -> None: ...

class GetDataByTypeRequest(_message.Message):
    __slots__ = ("mission_id", "type")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    type: DataType
    def __init__(self, mission_id: _Optional[str] = ..., type: _Optional[_Union[DataType, str]] = ...) -> None: ...

class GetDataByTypeResponse(_message.Message):
    __slots__ = ("success", "stored_data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STORED_DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    stored_data: StorageData
    def __init__(self, success: bool = ..., stored_data: _Optional[_Union[StorageData, _Mapping]] = ...) -> None: ...

class DeleteDataRequest(_message.Message):
    __slots__ = ("mission_id", "name")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DeleteDataResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
