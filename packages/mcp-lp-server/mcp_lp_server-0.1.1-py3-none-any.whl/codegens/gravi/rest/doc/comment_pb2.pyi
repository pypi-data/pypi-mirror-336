from gravi.models import gravi_model_pb2 as _gravi_model_pb2
from gravi.wrapper import wrappers_pb2 as _wrappers_pb2
import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateDocCommentResponseResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CreateDocCommentResponseResultSuccessful: _ClassVar[CreateDocCommentResponseResult]
    CreateDocCommentResponseResultDocumentNotFound: _ClassVar[CreateDocCommentResponseResult]
    CreateDocCommentResponseResultMalformedComment: _ClassVar[CreateDocCommentResponseResult]

class ListDocCommentsResponseResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ListDocCommentsResponseResultSuccessful: _ClassVar[ListDocCommentsResponseResult]
    ListDocCommentsResponseResultDocumentNotFound: _ClassVar[ListDocCommentsResponseResult]

class UpdateDocCommentResponseResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UpdateDocCommentResponseResultSuccessful: _ClassVar[UpdateDocCommentResponseResult]
    UpdateDocCommentResponseResultDocumentNotFound: _ClassVar[UpdateDocCommentResponseResult]
    UpdateDocCommentResponseResultCommentNotFound: _ClassVar[UpdateDocCommentResponseResult]
    UpdateDocCommentResponseResultOnlyAllowedForRootComment: _ClassVar[UpdateDocCommentResponseResult]
    UpdateDocCommentResponseResultMalformedComment: _ClassVar[UpdateDocCommentResponseResult]
CreateDocCommentResponseResultSuccessful: CreateDocCommentResponseResult
CreateDocCommentResponseResultDocumentNotFound: CreateDocCommentResponseResult
CreateDocCommentResponseResultMalformedComment: CreateDocCommentResponseResult
ListDocCommentsResponseResultSuccessful: ListDocCommentsResponseResult
ListDocCommentsResponseResultDocumentNotFound: ListDocCommentsResponseResult
UpdateDocCommentResponseResultSuccessful: UpdateDocCommentResponseResult
UpdateDocCommentResponseResultDocumentNotFound: UpdateDocCommentResponseResult
UpdateDocCommentResponseResultCommentNotFound: UpdateDocCommentResponseResult
UpdateDocCommentResponseResultOnlyAllowedForRootComment: UpdateDocCommentResponseResult
UpdateDocCommentResponseResultMalformedComment: UpdateDocCommentResponseResult

class DocCommentTO(_message.Message):
    __slots__ = ("id", "docId", "anchorId", "parentId", "authorPublicInfo", "isReadByMe", "isResolved", "createdOn", "lastModifiedOn", "payload", "isDeleted")
    ID_FIELD_NUMBER: _ClassVar[int]
    DOCID_FIELD_NUMBER: _ClassVar[int]
    ANCHORID_FIELD_NUMBER: _ClassVar[int]
    PARENTID_FIELD_NUMBER: _ClassVar[int]
    AUTHORPUBLICINFO_FIELD_NUMBER: _ClassVar[int]
    ISREADBYME_FIELD_NUMBER: _ClassVar[int]
    ISRESOLVED_FIELD_NUMBER: _ClassVar[int]
    CREATEDON_FIELD_NUMBER: _ClassVar[int]
    LASTMODIFIEDON_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ISDELETED_FIELD_NUMBER: _ClassVar[int]
    id: str
    docId: str
    anchorId: str
    parentId: str
    authorPublicInfo: _gravi_model_pb2.UserPublicTO
    isReadByMe: bool
    isResolved: bool
    createdOn: int
    lastModifiedOn: int
    payload: DocCommentPayload
    isDeleted: bool
    def __init__(self, id: _Optional[str] = ..., docId: _Optional[str] = ..., anchorId: _Optional[str] = ..., parentId: _Optional[str] = ..., authorPublicInfo: _Optional[_Union[_gravi_model_pb2.UserPublicTO, _Mapping]] = ..., isReadByMe: bool = ..., isResolved: bool = ..., createdOn: _Optional[int] = ..., lastModifiedOn: _Optional[int] = ..., payload: _Optional[_Union[DocCommentPayload, _Mapping]] = ..., isDeleted: bool = ...) -> None: ...

class UserMention(_message.Message):
    __slots__ = ("insertPos", "userPublicInfo")
    INSERTPOS_FIELD_NUMBER: _ClassVar[int]
    USERPUBLICINFO_FIELD_NUMBER: _ClassVar[int]
    insertPos: int
    userPublicInfo: _gravi_model_pb2.UserPublicTO
    def __init__(self, insertPos: _Optional[int] = ..., userPublicInfo: _Optional[_Union[_gravi_model_pb2.UserPublicTO, _Mapping]] = ...) -> None: ...

class DocCommentPayload(_message.Message):
    __slots__ = ("textCommentPayload",)
    TEXTCOMMENTPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    textCommentPayload: DocCommentPayloadTextComment
    def __init__(self, textCommentPayload: _Optional[_Union[DocCommentPayloadTextComment, _Mapping]] = ...) -> None: ...

class DocTextFragment(_message.Message):
    __slots__ = ("literal", "userId")
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    literal: str
    userId: str
    def __init__(self, literal: _Optional[str] = ..., userId: _Optional[str] = ...) -> None: ...

class DocCommentPayloadTextComment(_message.Message):
    __slots__ = ("content", "userMentions", "fragments")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    USERMENTIONS_FIELD_NUMBER: _ClassVar[int]
    FRAGMENTS_FIELD_NUMBER: _ClassVar[int]
    content: str
    userMentions: _containers.RepeatedCompositeFieldContainer[UserMention]
    fragments: _containers.RepeatedCompositeFieldContainer[DocTextFragment]
    def __init__(self, content: _Optional[str] = ..., userMentions: _Optional[_Iterable[_Union[UserMention, _Mapping]]] = ..., fragments: _Optional[_Iterable[_Union[DocTextFragment, _Mapping]]] = ...) -> None: ...

class CreateDocCommentRequest(_message.Message):
    __slots__ = ("docId", "anchorId", "parentId", "payload")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    ANCHORID_FIELD_NUMBER: _ClassVar[int]
    PARENTID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    docId: str
    anchorId: str
    parentId: str
    payload: DocCommentPayload
    def __init__(self, docId: _Optional[str] = ..., anchorId: _Optional[str] = ..., parentId: _Optional[str] = ..., payload: _Optional[_Union[DocCommentPayload, _Mapping]] = ...) -> None: ...

class CreateDocCommentResponse(_message.Message):
    __slots__ = ("result", "comment")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    result: CreateDocCommentResponseResult
    comment: DocCommentTO
    def __init__(self, result: _Optional[_Union[CreateDocCommentResponseResult, str]] = ..., comment: _Optional[_Union[DocCommentTO, _Mapping]] = ...) -> None: ...

class ListDocCommentsRequest(_message.Message):
    __slots__ = ("docId", "pageToken", "pageSize")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    docId: str
    pageToken: str
    pageSize: int
    def __init__(self, docId: _Optional[str] = ..., pageToken: _Optional[str] = ..., pageSize: _Optional[int] = ...) -> None: ...

class ListNewDocCommentsRequest(_message.Message):
    __slots__ = ("docId", "pageToken", "pageSize")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    PAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGESIZE_FIELD_NUMBER: _ClassVar[int]
    docId: str
    pageToken: str
    pageSize: int
    def __init__(self, docId: _Optional[str] = ..., pageToken: _Optional[str] = ..., pageSize: _Optional[int] = ...) -> None: ...

class ListDocCommentsResponse(_message.Message):
    __slots__ = ("result", "comments", "nextPageToken")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    NEXTPAGETOKEN_FIELD_NUMBER: _ClassVar[int]
    result: ListDocCommentsResponseResult
    comments: _containers.RepeatedCompositeFieldContainer[DocCommentTO]
    nextPageToken: str
    def __init__(self, result: _Optional[_Union[ListDocCommentsResponseResult, str]] = ..., comments: _Optional[_Iterable[_Union[DocCommentTO, _Mapping]]] = ..., nextPageToken: _Optional[str] = ...) -> None: ...

class UpdateDocCommentRequest(_message.Message):
    __slots__ = ("docId", "commentId", "isRead", "payload", "isResolved", "isDeleted")
    DOCID_FIELD_NUMBER: _ClassVar[int]
    COMMENTID_FIELD_NUMBER: _ClassVar[int]
    ISREAD_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ISRESOLVED_FIELD_NUMBER: _ClassVar[int]
    ISDELETED_FIELD_NUMBER: _ClassVar[int]
    docId: str
    commentId: str
    isRead: _wrappers_pb2.OptionalBool
    payload: DocCommentPayload
    isResolved: _wrappers_pb2.OptionalBool
    isDeleted: _wrappers_pb2.OptionalBool
    def __init__(self, docId: _Optional[str] = ..., commentId: _Optional[str] = ..., isRead: _Optional[_Union[_wrappers_pb2.OptionalBool, _Mapping]] = ..., payload: _Optional[_Union[DocCommentPayload, _Mapping]] = ..., isResolved: _Optional[_Union[_wrappers_pb2.OptionalBool, _Mapping]] = ..., isDeleted: _Optional[_Union[_wrappers_pb2.OptionalBool, _Mapping]] = ...) -> None: ...

class UpdateDocCommentResponse(_message.Message):
    __slots__ = ("result", "comment")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    result: UpdateDocCommentResponseResult
    comment: DocCommentTO
    def __init__(self, result: _Optional[_Union[UpdateDocCommentResponseResult, str]] = ..., comment: _Optional[_Union[DocCommentTO, _Mapping]] = ...) -> None: ...
