__version__ = "3.1.2"

from .DigitalAssistantCritic_pb2 import (
    DigitalAssistantCriticRequest,
    DigitalAssistantCriticResponse,
    ChatItem,
    InnerContextItem,
    OuterContextItem,
    ReplicaItem,
)

from .DigitalAssistantCritic_pb2_grpc import DigitalAssistantCriticStub
