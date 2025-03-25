import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AssetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AssetType_Unknown: _ClassVar[AssetType]
    AssetType_Obj: _ClassVar[AssetType]
    AssetType_Sketch: _ClassVar[AssetType]
    AssetType_Video: _ClassVar[AssetType]
    AssetType_Image: _ClassVar[AssetType]

class VideoType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VideoType_Unknown: _ClassVar[VideoType]
    VideoType_Skills: _ClassVar[VideoType]
    VideoType_Tutorials: _ClassVar[VideoType]
    VideoType_Beginner: _ClassVar[VideoType]
    VideoType_Marketing: _ClassVar[VideoType]
    VideoType_Pad_Tutorials: _ClassVar[VideoType]
    VideoType_VR_Tips: _ClassVar[VideoType]

class CoSketchRoomSize(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unknown: _ClassVar[CoSketchRoomSize]
    Small: _ClassVar[CoSketchRoomSize]
    Medium: _ClassVar[CoSketchRoomSize]
    Large: _ClassVar[CoSketchRoomSize]
    ExtraLarge: _ClassVar[CoSketchRoomSize]

class VideoCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VideoCategorySkills: _ClassVar[VideoCategory]
    VideoCategoryTutorials: _ClassVar[VideoCategory]
    VideoCategoryBeginner: _ClassVar[VideoCategory]
AssetType_Unknown: AssetType
AssetType_Obj: AssetType
AssetType_Sketch: AssetType
AssetType_Video: AssetType
AssetType_Image: AssetType
VideoType_Unknown: VideoType
VideoType_Skills: VideoType
VideoType_Tutorials: VideoType
VideoType_Beginner: VideoType
VideoType_Marketing: VideoType
VideoType_Pad_Tutorials: VideoType
VideoType_VR_Tips: VideoType
Unknown: CoSketchRoomSize
Small: CoSketchRoomSize
Medium: CoSketchRoomSize
Large: CoSketchRoomSize
ExtraLarge: CoSketchRoomSize
VideoCategorySkills: VideoCategory
VideoCategoryTutorials: VideoCategory
VideoCategoryBeginner: VideoCategory

class CmsContent(_message.Message):
    __slots__ = ("version", "canaryVersionUrl", "cosketchRoomPolicies", "priceTierPolicies", "coSketchRoomCosts", "marketingPopup")
    class CosketchRoomPoliciesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CoSketchRoomPolicy
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CoSketchRoomPolicy, _Mapping]] = ...) -> None: ...
    class PriceTierPoliciesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PriceTierPolicy
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[PriceTierPolicy, _Mapping]] = ...) -> None: ...
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CANARYVERSIONURL_FIELD_NUMBER: _ClassVar[int]
    COSKETCHROOMPOLICIES_FIELD_NUMBER: _ClassVar[int]
    PRICETIERPOLICIES_FIELD_NUMBER: _ClassVar[int]
    COSKETCHROOMCOSTS_FIELD_NUMBER: _ClassVar[int]
    MARKETINGPOPUP_FIELD_NUMBER: _ClassVar[int]
    version: str
    canaryVersionUrl: str
    cosketchRoomPolicies: _containers.MessageMap[str, CoSketchRoomPolicy]
    priceTierPolicies: _containers.MessageMap[str, PriceTierPolicy]
    coSketchRoomCosts: _containers.RepeatedCompositeFieldContainer[CoSketchRoomCost]
    marketingPopup: MarketingPopup
    def __init__(self, version: _Optional[str] = ..., canaryVersionUrl: _Optional[str] = ..., cosketchRoomPolicies: _Optional[_Mapping[str, CoSketchRoomPolicy]] = ..., priceTierPolicies: _Optional[_Mapping[str, PriceTierPolicy]] = ..., coSketchRoomCosts: _Optional[_Iterable[_Union[CoSketchRoomCost, _Mapping]]] = ..., marketingPopup: _Optional[_Union[MarketingPopup, _Mapping]] = ...) -> None: ...

class CmsAsset(_message.Message):
    __slots__ = ("title", "downloadUrl", "thumbnailUrl", "assetType", "videoType", "iPadTutorialKey", "priority", "hash")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    THUMBNAILURL_FIELD_NUMBER: _ClassVar[int]
    ASSETTYPE_FIELD_NUMBER: _ClassVar[int]
    VIDEOTYPE_FIELD_NUMBER: _ClassVar[int]
    IPADTUTORIALKEY_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    title: str
    downloadUrl: str
    thumbnailUrl: str
    assetType: AssetType
    videoType: VideoType
    iPadTutorialKey: str
    priority: int
    hash: str
    def __init__(self, title: _Optional[str] = ..., downloadUrl: _Optional[str] = ..., thumbnailUrl: _Optional[str] = ..., assetType: _Optional[_Union[AssetType, str]] = ..., videoType: _Optional[_Union[VideoType, str]] = ..., iPadTutorialKey: _Optional[str] = ..., priority: _Optional[int] = ..., hash: _Optional[str] = ...) -> None: ...

class MarketingPopup(_message.Message):
    __slots__ = ("title", "text", "video", "start", "end")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    title: str
    text: str
    video: CmsAsset
    start: int
    end: int
    def __init__(self, title: _Optional[str] = ..., text: _Optional[str] = ..., video: _Optional[_Union[CmsAsset, _Mapping]] = ..., start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class CoSketchRoomCost(_message.Message):
    __slots__ = ("size",)
    SIZE_FIELD_NUMBER: _ClassVar[int]
    size: CoSketchRoomSize
    def __init__(self, size: _Optional[_Union[CoSketchRoomSize, str]] = ...) -> None: ...

class CoSketchRoomPolicy(_message.Message):
    __slots__ = ("id", "maxUserCapPerRoom", "maxCoSketchRooms", "roomSize", "maxLaunchedRooms")
    ID_FIELD_NUMBER: _ClassVar[int]
    MAXUSERCAPPERROOM_FIELD_NUMBER: _ClassVar[int]
    MAXCOSKETCHROOMS_FIELD_NUMBER: _ClassVar[int]
    ROOMSIZE_FIELD_NUMBER: _ClassVar[int]
    MAXLAUNCHEDROOMS_FIELD_NUMBER: _ClassVar[int]
    id: str
    maxUserCapPerRoom: int
    maxCoSketchRooms: int
    roomSize: CoSketchRoomSize
    maxLaunchedRooms: int
    def __init__(self, id: _Optional[str] = ..., maxUserCapPerRoom: _Optional[int] = ..., maxCoSketchRooms: _Optional[int] = ..., roomSize: _Optional[_Union[CoSketchRoomSize, str]] = ..., maxLaunchedRooms: _Optional[int] = ...) -> None: ...

class PriceTierPolicy(_message.Message):
    __slots__ = ("id", "spaceAllowance")
    ID_FIELD_NUMBER: _ClassVar[int]
    SPACEALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    spaceAllowance: int
    def __init__(self, id: _Optional[str] = ..., spaceAllowance: _Optional[int] = ...) -> None: ...

class MenuGallery(_message.Message):
    __slots__ = ("version", "imageFolderUrl", "imageNames")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    IMAGEFOLDERURL_FIELD_NUMBER: _ClassVar[int]
    IMAGENAMES_FIELD_NUMBER: _ClassVar[int]
    version: int
    imageFolderUrl: str
    imageNames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, version: _Optional[int] = ..., imageFolderUrl: _Optional[str] = ..., imageNames: _Optional[_Iterable[str]] = ...) -> None: ...

class NoticeBoardLang(_message.Message):
    __slots__ = ("version", "langNum", "panelTitle", "pageTitle", "page1", "page2")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LANGNUM_FIELD_NUMBER: _ClassVar[int]
    PANELTITLE_FIELD_NUMBER: _ClassVar[int]
    PAGETITLE_FIELD_NUMBER: _ClassVar[int]
    PAGE1_FIELD_NUMBER: _ClassVar[int]
    PAGE2_FIELD_NUMBER: _ClassVar[int]
    version: int
    langNum: int
    panelTitle: str
    pageTitle: str
    page1: str
    page2: str
    def __init__(self, version: _Optional[int] = ..., langNum: _Optional[int] = ..., panelTitle: _Optional[str] = ..., pageTitle: _Optional[str] = ..., page1: _Optional[str] = ..., page2: _Optional[str] = ...) -> None: ...

class NoticeBoard(_message.Message):
    __slots__ = ("boards",)
    BOARDS_FIELD_NUMBER: _ClassVar[int]
    boards: _containers.RepeatedCompositeFieldContainer[NoticeBoardLang]
    def __init__(self, boards: _Optional[_Iterable[_Union[NoticeBoardLang, _Mapping]]] = ...) -> None: ...

class ObjAsset(_message.Message):
    __slots__ = ("name", "downloadUrl", "zipped", "grs")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    ZIPPED_FIELD_NUMBER: _ClassVar[int]
    GRS_FIELD_NUMBER: _ClassVar[int]
    name: str
    downloadUrl: str
    zipped: bool
    grs: bool
    def __init__(self, name: _Optional[str] = ..., downloadUrl: _Optional[str] = ..., zipped: bool = ..., grs: bool = ...) -> None: ...

class GallerySketch(_message.Message):
    __slots__ = ("name", "downloadUrl")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOWNLOADURL_FIELD_NUMBER: _ClassVar[int]
    name: str
    downloadUrl: str
    def __init__(self, name: _Optional[str] = ..., downloadUrl: _Optional[str] = ...) -> None: ...

class VideoDetails(_message.Message):
    __slots__ = ("title", "url", "category")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    title: str
    url: str
    category: VideoCategory
    def __init__(self, title: _Optional[str] = ..., url: _Optional[str] = ..., category: _Optional[_Union[VideoCategory, str]] = ...) -> None: ...

class CmsFeatureFlags(_message.Message):
    __slots__ = ("toolBeltBeta", "convertSubDRPCEnabled")
    TOOLBELTBETA_FIELD_NUMBER: _ClassVar[int]
    CONVERTSUBDRPCENABLED_FIELD_NUMBER: _ClassVar[int]
    toolBeltBeta: bool
    convertSubDRPCEnabled: bool
    def __init__(self, toolBeltBeta: bool = ..., convertSubDRPCEnabled: bool = ...) -> None: ...

class FontDetails(_message.Message):
    __slots__ = ("fontName", "url")
    FONTNAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    fontName: str
    url: str
    def __init__(self, fontName: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...
