import gs_options_pb2 as _gs_options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SatisfactionLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SatisfactionLevel_VeryPoor: _ClassVar[SatisfactionLevel]
    SatisfactionLevel_Poor: _ClassVar[SatisfactionLevel]
    SatisfactionLevel_Fair: _ClassVar[SatisfactionLevel]
    SatisfactionLevel_Good: _ClassVar[SatisfactionLevel]
    SatisfactionLevel_VeryGood: _ClassVar[SatisfactionLevel]

class FeedbackType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FeedbackType_Unknown: _ClassVar[FeedbackType]
    FeedbackType_Signup: _ClassVar[FeedbackType]
    FeedbackType_LandingPad: _ClassVar[FeedbackType]
    FeedbackType_CloudExport: _ClassVar[FeedbackType]
    FeedbackType_Free_Collab_Ten_Days_After_Creation: _ClassVar[FeedbackType]
    FeedbackTypeVRCollabExperience: _ClassVar[FeedbackType]

class SignupClient(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SignupClient_Unknown: _ClassVar[SignupClient]
    SignupClient_VR_Standalone: _ClassVar[SignupClient]
    SignupClient_iPad: _ClassVar[SignupClient]
    SignupClient_Web: _ClassVar[SignupClient]

class SignUpByEmailPassResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SignUpByEmailPassResult_UnknownError: _ClassVar[SignUpByEmailPassResult]
    SignUpByEmailPassResult_Success: _ClassVar[SignUpByEmailPassResult]
    SignUpByEmailPassResult_EmailAlreadyInUse: _ClassVar[SignUpByEmailPassResult]
    SignUpByEmailPassResult_FailedToSendEmail: _ClassVar[SignUpByEmailPassResult]
    SignUpByEmailPassResult_InvalidEmail: _ClassVar[SignUpByEmailPassResult]
    SignUpByEmailPassResult_InvalidPassword: _ClassVar[SignUpByEmailPassResult]
    SignUpByEmailPassResult_InvalidRecaptcha: _ClassVar[SignUpByEmailPassResult]

class ResendEmailVerificationResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ResendEmailVerificationResultUnknownError: _ClassVar[ResendEmailVerificationResult]
    ResendEmailVerificationResultSuccess: _ClassVar[ResendEmailVerificationResult]
    ResendEmailVerificationResultLinkMissing: _ClassVar[ResendEmailVerificationResult]

class InitiateSignUpType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InitiateSignUpTypeVive: _ClassVar[InitiateSignUpType]
    InitiateSignUpTypeFirstSketch: _ClassVar[InitiateSignUpType]

class InitiateSignUpResponseResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    InitiateSignUpResponseResultUnknown: _ClassVar[InitiateSignUpResponseResult]
    InitiateSignUpResponseResultSuccess: _ClassVar[InitiateSignUpResponseResult]
    InitiateSignUpResponseResultInvalidEmail: _ClassVar[InitiateSignUpResponseResult]
    InitiateSignUpResponseResultInvalidPayload: _ClassVar[InitiateSignUpResponseResult]
SatisfactionLevel_VeryPoor: SatisfactionLevel
SatisfactionLevel_Poor: SatisfactionLevel
SatisfactionLevel_Fair: SatisfactionLevel
SatisfactionLevel_Good: SatisfactionLevel
SatisfactionLevel_VeryGood: SatisfactionLevel
FeedbackType_Unknown: FeedbackType
FeedbackType_Signup: FeedbackType
FeedbackType_LandingPad: FeedbackType
FeedbackType_CloudExport: FeedbackType
FeedbackType_Free_Collab_Ten_Days_After_Creation: FeedbackType
FeedbackTypeVRCollabExperience: FeedbackType
SignupClient_Unknown: SignupClient
SignupClient_VR_Standalone: SignupClient
SignupClient_iPad: SignupClient
SignupClient_Web: SignupClient
SignUpByEmailPassResult_UnknownError: SignUpByEmailPassResult
SignUpByEmailPassResult_Success: SignUpByEmailPassResult
SignUpByEmailPassResult_EmailAlreadyInUse: SignUpByEmailPassResult
SignUpByEmailPassResult_FailedToSendEmail: SignUpByEmailPassResult
SignUpByEmailPassResult_InvalidEmail: SignUpByEmailPassResult
SignUpByEmailPassResult_InvalidPassword: SignUpByEmailPassResult
SignUpByEmailPassResult_InvalidRecaptcha: SignUpByEmailPassResult
ResendEmailVerificationResultUnknownError: ResendEmailVerificationResult
ResendEmailVerificationResultSuccess: ResendEmailVerificationResult
ResendEmailVerificationResultLinkMissing: ResendEmailVerificationResult
InitiateSignUpTypeVive: InitiateSignUpType
InitiateSignUpTypeFirstSketch: InitiateSignUpType
InitiateSignUpResponseResultUnknown: InitiateSignUpResponseResult
InitiateSignUpResponseResultSuccess: InitiateSignUpResponseResult
InitiateSignUpResponseResultInvalidEmail: InitiateSignUpResponseResult
InitiateSignUpResponseResultInvalidPayload: InitiateSignUpResponseResult

class SendUserFeedbackRequest(_message.Message):
    __slots__ = ("satisfactionLevel", "feedback", "feedbackType", "vrCollabExperienceFeedbackPayload")
    SATISFACTIONLEVEL_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    FEEDBACKTYPE_FIELD_NUMBER: _ClassVar[int]
    VRCOLLABEXPERIENCEFEEDBACKPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    satisfactionLevel: SatisfactionLevel
    feedback: str
    feedbackType: FeedbackType
    vrCollabExperienceFeedbackPayload: VRCollabExperienceFeedbackPayload
    def __init__(self, satisfactionLevel: _Optional[_Union[SatisfactionLevel, str]] = ..., feedback: _Optional[str] = ..., feedbackType: _Optional[_Union[FeedbackType, str]] = ..., vrCollabExperienceFeedbackPayload: _Optional[_Union[VRCollabExperienceFeedbackPayload, _Mapping]] = ...) -> None: ...

class VRCollabExperienceFeedbackPayload(_message.Message):
    __slots__ = ("roomId", "roomSessionId")
    ROOMID_FIELD_NUMBER: _ClassVar[int]
    ROOMSESSIONID_FIELD_NUMBER: _ClassVar[int]
    roomId: str
    roomSessionId: str
    def __init__(self, roomId: _Optional[str] = ..., roomSessionId: _Optional[str] = ...) -> None: ...

class SendUserFeedbackResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SignUpByEmailPassRequest(_message.Message):
    __slots__ = ("email", "encryptedPass", "firstName", "lastName", "signupClient", "lastLocation", "reCaptchaToken", "activateLinkCode")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTEDPASS_FIELD_NUMBER: _ClassVar[int]
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    SIGNUPCLIENT_FIELD_NUMBER: _ClassVar[int]
    LASTLOCATION_FIELD_NUMBER: _ClassVar[int]
    RECAPTCHATOKEN_FIELD_NUMBER: _ClassVar[int]
    ACTIVATELINKCODE_FIELD_NUMBER: _ClassVar[int]
    email: str
    encryptedPass: bytes
    firstName: str
    lastName: str
    signupClient: SignupClient
    lastLocation: str
    reCaptchaToken: str
    activateLinkCode: str
    def __init__(self, email: _Optional[str] = ..., encryptedPass: _Optional[bytes] = ..., firstName: _Optional[str] = ..., lastName: _Optional[str] = ..., signupClient: _Optional[_Union[SignupClient, str]] = ..., lastLocation: _Optional[str] = ..., reCaptchaToken: _Optional[str] = ..., activateLinkCode: _Optional[str] = ...) -> None: ...

class SignUpByEmailPassResponse(_message.Message):
    __slots__ = ("verifyCode", "result")
    VERIFYCODE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    verifyCode: str
    result: SignUpByEmailPassResult
    def __init__(self, verifyCode: _Optional[str] = ..., result: _Optional[_Union[SignUpByEmailPassResult, str]] = ...) -> None: ...

class ResendEmailVerificationRequest(_message.Message):
    __slots__ = ("queryCode",)
    QUERYCODE_FIELD_NUMBER: _ClassVar[int]
    queryCode: str
    def __init__(self, queryCode: _Optional[str] = ...) -> None: ...

class ResendEmailVerificationResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ResendEmailVerificationResult
    def __init__(self, result: _Optional[_Union[ResendEmailVerificationResult, str]] = ...) -> None: ...

class InitiateSignUpRequest(_message.Message):
    __slots__ = ("email", "signUpType", "firstSketchPayload")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    SIGNUPTYPE_FIELD_NUMBER: _ClassVar[int]
    FIRSTSKETCHPAYLOAD_FIELD_NUMBER: _ClassVar[int]
    email: str
    signUpType: InitiateSignUpType
    firstSketchPayload: InitiateSignUpPayloadFirstSketch
    def __init__(self, email: _Optional[str] = ..., signUpType: _Optional[_Union[InitiateSignUpType, str]] = ..., firstSketchPayload: _Optional[_Union[InitiateSignUpPayloadFirstSketch, _Mapping]] = ...) -> None: ...

class InitiateSignUpPayloadFirstSketch(_message.Message):
    __slots__ = ("imageBytes",)
    IMAGEBYTES_FIELD_NUMBER: _ClassVar[int]
    imageBytes: bytes
    def __init__(self, imageBytes: _Optional[bytes] = ...) -> None: ...

class InitiateSignUpResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: InitiateSignUpResponseResult
    def __init__(self, result: _Optional[_Union[InitiateSignUpResponseResult, str]] = ...) -> None: ...
