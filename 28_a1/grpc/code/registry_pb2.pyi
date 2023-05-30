from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EnquireServers(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class LiveServer(_message.Message):
    __slots__ = ["Server"]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    Server: str
    def __init__(self, Server: _Optional[str] = ...) -> None: ...

class RegistryResponseStatus(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class ServerAddress(_message.Message):
    __slots__ = ["IP", "Port", "ServerName"]
    IP: str
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    Port: int
    SERVERNAME_FIELD_NUMBER: _ClassVar[int]
    ServerName: str
    def __init__(self, ServerName: _Optional[str] = ..., IP: _Optional[str] = ..., Port: _Optional[int] = ...) -> None: ...
