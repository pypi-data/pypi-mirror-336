import asyncio
import grpc
import logging
from concurrent import futures
from typing import Optional
from .proto_gen import character_worker_pb2_grpc
from .worker_service import CharacterWorkerService
from .character_state import CharacterState

DEFAULT_PORT = "50051"
DEFAULT_WORKERS = 10
logger = logging.getLogger(__name__)


class CharacterWorker:
    """
    CharacterWorker: state machine designed to handle multiple character states
    and manage their transitions during a conversation.

    Attributes:
        states (list[CharacterState]): A list of available character states.
        init_state (CharacterState): The initial state to begin with.
    """

    def __init__(self) -> None:
        self.states: list[CharacterState] = []
        self.init_state: CharacterState = None

    def run(
        self,
        port: Optional[str] = DEFAULT_PORT,
        max_workers: Optional[int] = DEFAULT_WORKERS,
    ):
        """
        Runs the character worker. Ensures that the required states
        and initial state are provided before starting the server.

        Args:
            port (str, optional): The port to bind the gRPC server to. Defaults to "50051".
            max_workers (int, optional): The maximum number of workers for the gRPC server. Defaults to 10.

        Returns:
            None
        """
        if len(self.states) == 0:
            logger.error("Please define states")
            return

        if self.init_state is None:
            logger.error("Please define initial state")
            return

        self.loop = asyncio.new_event_loop()

        logger.info("Starting Character Worker...")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        character_worker_pb2_grpc.add_CharacterWorkerServiceServicer_to_server(
            CharacterWorkerService(
                init_state=self.init_state,
                states=self.states,
                loop=self.loop,
            ),
            server,
        )
        server.add_insecure_port("[::]:" + port)
        server.start()
        logger.info("worker started: " + port)
        server.wait_for_termination()
