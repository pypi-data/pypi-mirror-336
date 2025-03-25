import json
import logging
import grpc
from enum import Enum
from typing import Any, Optional
from .character_intent import MatchIntentResult, SetGuidelinesResult
from .character_memory import CharacterMemory
from .character_vision import CharacterVision
from ..proto_gen.character_vision_pb2_grpc import VisionServiceStub
from ..proto_gen.notification_service_pb2_grpc import CharacterNotificationServiceStub
from ..proto_gen.interaction_service_pb2_grpc import CharacterInteractionServiceStub
from ..proto_gen.character_vision_pb2 import VisionRequest
from ..proto_gen.notification_service_pb2 import NotificationRequest
from ..proto_gen.interaction_service_pb2 import InteractionRequest

logger = logging.getLogger(__name__)


class CharacterResponseStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class CharacterContext:

    def __init__(
        self,
        interaction_id,
        state,
        args,
        response_message,
        state_description,
        next,
        grpc_service_url=None,
    ):
        self.interaction_id = interaction_id
        self.state = state
        self.state_description = state_description
        self.args = args
        self.next = next
        self.response_status: CharacterResponseStatus = CharacterResponseStatus.SUCCESS
        self.response_message = response_message
        self.memory = CharacterMemory(interaction_id=interaction_id)
        self._grpc_service_url = grpc_service_url

    def set_state(self, state):
        self.state = state
        self.state_description = getattr(type(state), "_state_description", "")

    def set_response(
        self,
        response_status: CharacterResponseStatus,
        response_message: Optional[str] = None,
    ):
        self.response_status = response_status
        self.response_message = response_message

    def get_args(self):
        return self.args

    def get_memory(self) -> CharacterMemory:
        return self.memory

    def end_interaction(self, force: Optional[bool] = False) -> None:
        logger.debug("REQ :: end_interaction")

        self.channel = (
            grpc.insecure_channel(self._grpc_service_url)
            if self._grpc_service_url is not None
            else None
        )
        CharacterInteractionServiceStub(self.channel).HandleInteraction(
            InteractionRequest(
                interaction_id=self.interaction_id,
                event="end_interaction",
                args=json.dumps({"forceFully": force}),
            )
        )

    def match_intent(self, query: str) -> MatchIntentResult:
        logger.debug("REQ :: match_intent")
        self.channel = (
            grpc.insecure_channel(self._grpc_service_url)
            if self._grpc_service_url is not None
            else None
        )

        res = CharacterInteractionServiceStub(self.channel).HandleInteraction(
            InteractionRequest(
                interaction_id=self.interaction_id,
                event="match_intent",
                args=json.dumps({"query": query}),
            )
        )
        response = json.loads(res.response)
        data = response["data"]

        return MatchIntentResult(success=data["success"], score=data["score"])

    def set_guidelines(self, guidelines: list[str] = []) -> SetGuidelinesResult:
        logger.debug("REQ :: set_guidelines")
        self.channel = (
            grpc.insecure_channel(self._grpc_service_url)
            if self._grpc_service_url is not None
            else None
        )

        res = CharacterInteractionServiceStub(self.channel).HandleInteraction(
            InteractionRequest(
                interaction_id=self.interaction_id,
                event="set_guidelines",
                args=json.dumps({"guidelines": guidelines}),
            )
        )
        response = json.loads(res.response)
        data = response["data"]
        return SetGuidelinesResult(success=data["success"], message=data["message"])

    def get_vision(self) -> CharacterVision:
        logger.debug("REQ :: get_vision")
        self.channel = (
            grpc.insecure_channel(self._grpc_service_url)
            if self._grpc_service_url is not None
            else None
        )
        res = VisionServiceStub(self.channel).HandleVision(
            VisionRequest(
                interaction_id=self.interaction_id,
                current_state_name=type(self.state).__name__,
            )
        )
        return CharacterVision(
            success=res.success,
            message=res.message,
            image=res.image,
        )

    def broadcast(self, topic: str, data: dict[str, Any]):
        logger.debug("REQ :: broadcast")
        self.channel = (
            grpc.insecure_channel(self._grpc_service_url)
            if self._grpc_service_url is not None
            else None
        )
        CharacterNotificationServiceStub(self.channel).HandleNotification(
            NotificationRequest(
                interaction_id=self.interaction_id,
                current_state_name=type(self.state).__name__,
                topic=topic,
                data=json.dumps(data),
            )
        )
