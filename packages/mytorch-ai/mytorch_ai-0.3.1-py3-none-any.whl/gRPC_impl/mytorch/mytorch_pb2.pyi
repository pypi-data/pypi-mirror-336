from gRPC_impl import shared_msg_types_pb2 as _shared_msg_types_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ARangeRequest(_message.Message):
    __slots__ = ("start", "end", "step")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    start: float
    end: float
    step: float
    def __init__(self, start: _Optional[float] = ..., end: _Optional[float] = ..., step: _Optional[float] = ...) -> None: ...

class ArgMaxRequest(_message.Message):
    __slots__ = ("tensor_uuid", "dim", "keepdim")
    TENSOR_UUID_FIELD_NUMBER: _ClassVar[int]
    DIM_FIELD_NUMBER: _ClassVar[int]
    KEEPDIM_FIELD_NUMBER: _ClassVar[int]
    tensor_uuid: str
    dim: int
    keepdim: bool
    def __init__(self, tensor_uuid: _Optional[str] = ..., dim: _Optional[int] = ..., keepdim: bool = ...) -> None: ...

class AllCloseRequest(_message.Message):
    __slots__ = ("tensor1_uuid", "tensor2_uuid", "rtol", "atol", "equal_nan")
    TENSOR1_UUID_FIELD_NUMBER: _ClassVar[int]
    TENSOR2_UUID_FIELD_NUMBER: _ClassVar[int]
    RTOL_FIELD_NUMBER: _ClassVar[int]
    ATOL_FIELD_NUMBER: _ClassVar[int]
    EQUAL_NAN_FIELD_NUMBER: _ClassVar[int]
    tensor1_uuid: str
    tensor2_uuid: str
    rtol: float
    atol: float
    equal_nan: bool
    def __init__(self, tensor1_uuid: _Optional[str] = ..., tensor2_uuid: _Optional[str] = ..., rtol: _Optional[float] = ..., atol: _Optional[float] = ..., equal_nan: bool = ...) -> None: ...

class RepeatInterleaveRequest(_message.Message):
    __slots__ = ("tensor_uuid", "repeats", "dim")
    TENSOR_UUID_FIELD_NUMBER: _ClassVar[int]
    REPEATS_FIELD_NUMBER: _ClassVar[int]
    DIM_FIELD_NUMBER: _ClassVar[int]
    tensor_uuid: str
    repeats: int
    dim: int
    def __init__(self, tensor_uuid: _Optional[str] = ..., repeats: _Optional[int] = ..., dim: _Optional[int] = ...) -> None: ...
