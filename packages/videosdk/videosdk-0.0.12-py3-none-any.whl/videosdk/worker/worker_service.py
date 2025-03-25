import json
import logging
from asyncio import AbstractEventLoop, Event
from concurrent.futures import ThreadPoolExecutor
from .character_state import CharacterState
from .context import CharacterContext, CharacterResponseStatus
from .proto_gen import character_worker_pb2_grpc, character_worker_pb2

logger = logging.getLogger(__name__)


class CharacterWorkerService(character_worker_pb2_grpc.CharacterWorkerService):

    def __init__(
        self,
        init_state: CharacterState,
        states: list[CharacterState],
        loop: AbstractEventLoop,
    ) -> None:
        self.init_state = init_state
        self.states = states
        self.state_map = {}
        self.loop = loop
        for index, state in enumerate(self.states):
            self.state_map[type(state).__name__] = index

    def HandleState(self, request, grpc_context):
        res = self.loop.run_until_complete(
            self.HandleStateAsync(request=request, grpc_context=grpc_context)
        )
        logger.debug(f"Response from handle() {res}")
        return character_worker_pb2.StateResponse(
            interaction_id=res["interaction_id"],
            next_state=res["next_state"],
            next_state_description=res["next_state_description"],
            next_state_params=res["next_state_params"],
            response_status=res["response_status"],
            response_message=res["response_message"],
        )

    def get_state_by_name(self, state_name) -> CharacterState:
        index = self.state_map[state_name]
        return self.states[index]

    async def HandleStateAsync(self, request, grpc_context):
        try:
            interaction_id = request.interaction_id
            current_state_name = request.current_state_name
            current_state_description = request.current_state_description
            current_state_args = json.loads(request.current_state_args)
            grpc_service_url = request.grpc_service_url

            logger.debug(
                f"Request received {interaction_id}, {current_state_name}, {current_state_args}"
            )

            next_event = Event()

            def next():
                next_event.set()

            if current_state_name != "":
                current_state = self.get_state_by_name(state_name=current_state_name)
                context = CharacterContext(
                    interaction_id=interaction_id,
                    state=current_state_name,
                    state_description=current_state_description,
                    response_message="",
                    grpc_service_url=grpc_service_url,
                    next=next,
                    args=current_state_args,
                )
                with ThreadPoolExecutor() as executor:
                    await self.loop.run_in_executor(
                        executor, current_state.handle, context
                    )
                await next_event.wait()
                next_state = type(context.state).__name__
                next_state_description = getattr(
                    context.state, "_state_description", ""
                )
                next_state_params = json.dumps(
                    getattr(context.state, "_state_params", {})
                )
                response_status = context.response_status
                response_message = context.response_message
            else:
                next_state = type(self.init_state).__name__
                next_state_description = getattr(
                    self.init_state, "_state_description", ""
                )
                next_state_params = json.dumps(
                    getattr(self.init_state, "_state_params", {})
                )
                response_status = CharacterResponseStatus.SUCCESS
                response_message = ""

            logger.debug(f"Next state  {next_state_description}")

            return {
                "interaction_id": interaction_id,
                "next_state": next_state,
                "next_state_description": next_state_description,
                "next_state_params": next_state_params,
                "response_status": response_status.name,
                "response_message": response_message,
            }
        except Exception as e:
            raise (f"Error in State Handling :: {e}")
