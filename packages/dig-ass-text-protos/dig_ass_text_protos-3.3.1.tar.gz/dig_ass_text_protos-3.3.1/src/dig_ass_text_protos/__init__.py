__version__ = "3.3.1"

from .DigitalAssistantText_pb2 import (
    DigitalAssistantTextRequest,
    DigitalAssistantTextResponse,
    ChatItem,
    InnerContextItem,
    OuterContextItem,
    ReplicaItem,
)

from .DigitalAssistantText_pb2_grpc import DigitalAssistantTextStub
