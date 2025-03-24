from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    upload: _ClassVar[FileAction]
    download: _ClassVar[FileAction]

class FileErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NoError: _ClassVar[FileErrorCode]
    IOError: _ClassVar[FileErrorCode]
    NoPermission: _ClassVar[FileErrorCode]
    ProtoError: _ClassVar[FileErrorCode]
    InvalidEnd: _ClassVar[FileErrorCode]
    FileError: _ClassVar[FileErrorCode]
    InvalidFileName: _ClassVar[FileErrorCode]
    WrongLength: _ClassVar[FileErrorCode]
    RoomNotExist: _ClassVar[FileErrorCode]
    UnexpectedFileEnd: _ClassVar[FileErrorCode]
upload: FileAction
download: FileAction
NoError: FileErrorCode
IOError: FileErrorCode
NoPermission: FileErrorCode
ProtoError: FileErrorCode
InvalidEnd: FileErrorCode
FileError: FileErrorCode
InvalidFileName: FileErrorCode
WrongLength: FileErrorCode
RoomNotExist: FileErrorCode
UnexpectedFileEnd: FileErrorCode

class FileHeader(_message.Message):
    __slots__ = ("filename", "startPos", "endPos", "secretCode", "finishFileName", "action", "roomId")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    STARTPOS_FIELD_NUMBER: _ClassVar[int]
    ENDPOS_FIELD_NUMBER: _ClassVar[int]
    SECRETCODE_FIELD_NUMBER: _ClassVar[int]
    FINISHFILENAME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    filename: str
    startPos: int
    endPos: int
    secretCode: str
    finishFileName: str
    action: FileAction
    roomId: str
    def __init__(self, filename: _Optional[str] = ..., startPos: _Optional[int] = ..., endPos: _Optional[int] = ..., secretCode: _Optional[str] = ..., finishFileName: _Optional[str] = ..., action: _Optional[_Union[FileAction, str]] = ..., roomId: _Optional[str] = ...) -> None: ...

class FileResponse(_message.Message):
    __slots__ = ("filename", "startPos", "endPos", "errorCode", "action")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    STARTPOS_FIELD_NUMBER: _ClassVar[int]
    ENDPOS_FIELD_NUMBER: _ClassVar[int]
    ERRORCODE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    filename: str
    startPos: int
    endPos: int
    errorCode: FileErrorCode
    action: FileAction
    def __init__(self, filename: _Optional[str] = ..., startPos: _Optional[int] = ..., endPos: _Optional[int] = ..., errorCode: _Optional[_Union[FileErrorCode, str]] = ..., action: _Optional[_Union[FileAction, str]] = ...) -> None: ...
