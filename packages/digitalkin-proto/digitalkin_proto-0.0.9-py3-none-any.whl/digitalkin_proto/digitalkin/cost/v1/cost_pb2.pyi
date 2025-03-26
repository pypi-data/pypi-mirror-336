from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CostType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OTHER: _ClassVar[CostType]
    TOKEN_INPUT: _ClassVar[CostType]
    TOKEN_OUTPUT: _ClassVar[CostType]
    API_CALL: _ClassVar[CostType]
    STORAGE: _ClassVar[CostType]
    TIME: _ClassVar[CostType]
OTHER: CostType
TOKEN_INPUT: CostType
TOKEN_OUTPUT: CostType
API_CALL: CostType
STORAGE: CostType
TIME: CostType

class Cost(_message.Message):
    __slots__ = ("cost", "mission_id", "name", "type", "unit")
    COST_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    cost: float
    mission_id: str
    name: str
    type: CostType
    unit: str
    def __init__(self, cost: _Optional[float] = ..., mission_id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[CostType, str]] = ..., unit: _Optional[str] = ...) -> None: ...

class AddCostRequest(_message.Message):
    __slots__ = ("cost", "mission_id", "name", "type", "unit")
    COST_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    cost: float
    mission_id: str
    name: str
    type: CostType
    unit: str
    def __init__(self, cost: _Optional[float] = ..., mission_id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[CostType, str]] = ..., unit: _Optional[str] = ...) -> None: ...

class AddCostResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class GetCostsByMissionRequest(_message.Message):
    __slots__ = ("mission_id",)
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    def __init__(self, mission_id: _Optional[str] = ...) -> None: ...

class GetCostsByMissionResponse(_message.Message):
    __slots__ = ("costs",)
    COSTS_FIELD_NUMBER: _ClassVar[int]
    costs: _containers.RepeatedCompositeFieldContainer[Cost]
    def __init__(self, costs: _Optional[_Iterable[_Union[Cost, _Mapping]]] = ...) -> None: ...

class GetCostsByNameRequest(_message.Message):
    __slots__ = ("mission_id", "name")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetCostsByNameResponse(_message.Message):
    __slots__ = ("costs",)
    COSTS_FIELD_NUMBER: _ClassVar[int]
    costs: _containers.RepeatedCompositeFieldContainer[Cost]
    def __init__(self, costs: _Optional[_Iterable[_Union[Cost, _Mapping]]] = ...) -> None: ...

class GetCostsByTypeRequest(_message.Message):
    __slots__ = ("mission_id", "type")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    type: CostType
    def __init__(self, mission_id: _Optional[str] = ..., type: _Optional[_Union[CostType, str]] = ...) -> None: ...

class GetCostsByTypeResponse(_message.Message):
    __slots__ = ("costs",)
    COSTS_FIELD_NUMBER: _ClassVar[int]
    costs: _containers.RepeatedCompositeFieldContainer[Cost]
    def __init__(self, costs: _Optional[_Iterable[_Union[Cost, _Mapping]]] = ...) -> None: ...
