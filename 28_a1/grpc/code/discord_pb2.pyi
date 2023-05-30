from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArticleFormat(_message.Message):
    __slots__ = ["Author", "Content", "FASHION", "POLITICS", "PublisherId", "SPORTS", "Timestamp", "status"]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    Author: str
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    Content: str
    FASHION: bool
    FASHION_FIELD_NUMBER: _ClassVar[int]
    POLITICS: bool
    POLITICS_FIELD_NUMBER: _ClassVar[int]
    PUBLISHERID_FIELD_NUMBER: _ClassVar[int]
    PublisherId: ClientIdentifier
    SPORTS: bool
    SPORTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    Timestamp: str
    status: str
    def __init__(self, SPORTS: bool = ..., FASHION: bool = ..., POLITICS: bool = ..., Author: _Optional[str] = ..., Content: _Optional[str] = ..., Timestamp: _Optional[str] = ..., PublisherId: _Optional[_Union[ClientIdentifier, _Mapping]] = ..., status: _Optional[str] = ...) -> None: ...

class ArticleTag(_message.Message):
    __slots__ = ["Author", "Content", "FASHION", "POLITICS", "PublisherId", "SPORTS", "Timestamp"]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    Author: str
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    Content: str
    FASHION: bool
    FASHION_FIELD_NUMBER: _ClassVar[int]
    POLITICS: bool
    POLITICS_FIELD_NUMBER: _ClassVar[int]
    PUBLISHERID_FIELD_NUMBER: _ClassVar[int]
    PublisherId: ClientIdentifier
    SPORTS: bool
    SPORTS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    Timestamp: str
    def __init__(self, SPORTS: bool = ..., FASHION: bool = ..., POLITICS: bool = ..., Author: _Optional[str] = ..., Content: _Optional[str] = ..., Timestamp: _Optional[str] = ..., PublisherId: _Optional[_Union[ClientIdentifier, _Mapping]] = ...) -> None: ...

class ClientIdentifier(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class HealthCheckRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ["servingstatus"]
    SERVINGSTATUS_FIELD_NUMBER: _ClassVar[int]
    servingstatus: bool
    def __init__(self, servingstatus: bool = ...) -> None: ...

class ResponseStatus(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
