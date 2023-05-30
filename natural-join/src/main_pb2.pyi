from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterRequest(_message.Message):
    __slots__ = ["ip", "port", "type"]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ip: str
    port: str
    type: str
    def __init__(self, ip: _Optional[str] = ..., port: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ["id", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    def __init__(self, status: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class SubmissionRequest(_message.Message):
    __slots__ = ["id", "outputPath", "reducerPaths", "status", "type"]
    class ReducerPathsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTPATH_FIELD_NUMBER: _ClassVar[int]
    REDUCERPATHS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    outputPath: str
    reducerPaths: _containers.ScalarMap[str, str]
    status: str
    type: str
    def __init__(self, type: _Optional[str] = ..., status: _Optional[str] = ..., id: _Optional[str] = ..., outputPath: _Optional[str] = ..., reducerPaths: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SubmissionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WorkerReadyRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WorkerReadyResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
