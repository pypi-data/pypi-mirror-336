from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalAssistantChatManagerRequest(_message.Message):
    __slots__ = ("Text", "OuterContext", "RequestId", "ResourceId")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    OUTERCONTEXT_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Text: str
    OuterContext: OuterContextItem
    RequestId: str
    ResourceId: str
    def __init__(self, Text: _Optional[str] = ..., OuterContext: _Optional[_Union[OuterContextItem, _Mapping]] = ..., RequestId: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...

class DigitalAssistantChatManagerResponse(_message.Message):
    __slots__ = ("Text", "State", "Action")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    Text: str
    State: str
    Action: str
    def __init__(self, Text: _Optional[str] = ..., State: _Optional[str] = ..., Action: _Optional[str] = ...) -> None: ...

class OuterContextItem(_message.Message):
    __slots__ = ("Sex", "Age", "UserId", "SessionId", "ClientId", "TrackId")
    SEX_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    SESSIONID_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    TRACKID_FIELD_NUMBER: _ClassVar[int]
    Sex: bool
    Age: int
    UserId: str
    SessionId: str
    ClientId: str
    TrackId: str
    def __init__(self, Sex: bool = ..., Age: _Optional[int] = ..., UserId: _Optional[str] = ..., SessionId: _Optional[str] = ..., ClientId: _Optional[str] = ..., TrackId: _Optional[str] = ...) -> None: ...
