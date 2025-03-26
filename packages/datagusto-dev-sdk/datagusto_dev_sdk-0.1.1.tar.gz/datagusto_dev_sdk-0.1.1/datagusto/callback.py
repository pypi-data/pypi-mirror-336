import logging
from typing import Any
from uuid import UUID
import os
import httpx

from langchain.callbacks.base import (
    BaseCallbackHandler as LangchainBaseCallbackHandler,
)
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk, LLMResult

from .client import DatagustoClient, ObservationType, TraceCreate, TraceUpdate, ObservationCreate, TraceStatus


class DatagustoBaseCallbackHandler:
    def __init__(
        self,
        *,
        secret_key: str | None = None,
        host: str | None = None,
        debug: bool | None = None,
        session_id: str | None = None,
        trace_name: str | None = None,
        metadata: Any | None = None,
        tags: list[str] | None = None,
        max_retries: int | None = None,
        timeout: int | None = None,
        httpx_client: httpx.Client | None = None,
        **kwargs,
    ):
        self.session_id = session_id
        self.trace_name = trace_name
        self.metadata = metadata
        self.tags = tags

        secret_key = secret_key or os.environ.get("DATAGUSTO_SECRET_KEY")
        host = host or os.environ.get("DATAGUSTO_HOST", "https://cloud.datagusto.ai")

        if not secret_key:
            raise ValueError("secret_key is required")

        is_debug_mode = (
            debug if debug else (os.environ.get("DATAGUSTO_DEBUG", "False") == "True")
        )
        if is_debug_mode:
            logging.basicConfig()
            logging.getLogger("datagusto").setLevel(logging.DEBUG)
        else:
            logging.getLogger("datagusto").setLevel(logging.WARNING)

        # stateful client
        self.client = DatagustoClient(base_url=host, api_key=secret_key)
        self.current_trace_id = None
        self.runs = {}


class LangchainCallbackHandler(
    LangchainBaseCallbackHandler, DatagustoBaseCallbackHandler
):
    log = logging.getLogger("datagusto")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_trace_id = None

    def on_agent_action(self, action, **kwargs):
        self._log_debug_event("Agent action", kwargs.get("run_id"), kwargs.get("parent_run_id"), **kwargs)
        # TODO: Implement agent action

    def on_agent_finish(self, finish, **kwargs):
        self._log_debug_event("Agent finish", kwargs.get("run_id"), kwargs.get("parent_run_id"), **kwargs)
        # TODO: Implement agent finish

    def on_chain_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        try:
            self._log_debug_event("Chain start", run_id, parent_run_id, **kwargs)
            self._ensure_trace_exists(run_id, parent_run_id, serialized=serialized, inputs=inputs, metadata=metadata, **kwargs)
            
            if self.current_trace_id:
                # Include serialized and other info in metadata
                observation_metadata = metadata or {}
                observation_metadata["serialized"] = serialized
                observation_metadata.update({k: v for k, v in kwargs.items() if k not in ["name"]})
                
                # Ensure inputs is a dictionary - convert it if it's not
                input_dict = {}
                if isinstance(inputs, dict):
                    input_dict = inputs
                else:
                    # Handle non-dictionary inputs by creating a structured representation
                    input_dict = {"raw_input": str(inputs)}
                
                observation = ObservationCreate(
                    type=ObservationType.OTHER,
                    name=self.get_langchain_run_name(serialized, **kwargs),
                    input=input_dict,
                    observation_metadata=observation_metadata,
                    parent_id=str(parent_run_id) if parent_run_id else None,
                    run_id=str(run_id)
                )
                self.client.add_observation(self.current_trace_id, observation)

        except Exception as e:
            self.log.error(f"Error in on_chain_start: {e}")


    def on_chain_end(
        self,
        outputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("Chain end", run_id, parent_run_id, **kwargs)
        
        if self.current_trace_id:
            observation = ObservationCreate(
                type=ObservationType.OTHER,
                name="chain_end",
                input={},
                output=outputs,
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_chain_error(
        self,
        error: Exception | KeyboardInterrupt,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("Chain error", run_id, parent_run_id, **kwargs)
        
        if self.current_trace_id:
            observation = ObservationCreate(
                type=ObservationType.OTHER,
                name="chain_error",
                input={},
                output={"error": str(error)},
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)
            
            # Mark trace as error
            self.client.complete_trace(self.current_trace_id, TraceUpdate(
                status=TraceStatus.ERROR,
                trace_metadata={"error": str(error)}
            ))

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("Chat model start", run_id, parent_run_id, **kwargs)
        self._ensure_trace_exists(run_id, parent_run_id, serialized=serialized, inputs=inputs, **kwargs)
        
        if self.current_trace_id:
            # Include serialized and other info in metadata
            observation_metadata = {}
            observation_metadata["serialized"] = serialized
            observation_metadata.update({k: v for k, v in kwargs.items() if k not in ["name"]})
            
            # Ensure inputs is a dictionary - convert it if it's not
            input_dict = {}
            if isinstance(inputs, dict):
                input_dict = inputs
            else:
                # Handle non-dictionary inputs by creating a structured representation
                input_dict = {"raw_input": str(inputs)}
            
            observation = ObservationCreate(
                type=ObservationType.LLM,
                name=self.get_langchain_run_name(serialized, **kwargs),
                input=input_dict,
                observation_metadata=observation_metadata,
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("LLM start", run_id, parent_run_id, **kwargs)
        self._ensure_trace_exists(run_id, parent_run_id, serialized=serialized, inputs=inputs, **kwargs)
        
        if self.current_trace_id:
            # Include serialized and other info in metadata
            observation_metadata = {}
            observation_metadata["serialized"] = serialized
            observation_metadata.update({k: v for k, v in kwargs.items() if k not in ["name"]})
            
            # Ensure inputs is a dictionary - convert it if it's not
            input_dict = {}
            if isinstance(inputs, dict):
                input_dict = inputs
            else:
                # Handle non-dictionary inputs by creating a structured representation
                input_dict = {"raw_input": str(inputs)}
            
            observation = ObservationCreate(
                type=ObservationType.LLM,
                name=self.get_langchain_run_name(serialized, **kwargs),
                input=input_dict,
                observation_metadata=observation_metadata,
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: GenerationChunk | ChatGenerationChunk | None = None,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("LLM new token", run_id, parent_run_id, **kwargs)
        # Token streaming is not recorded to avoid too many API calls

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("LLM end", run_id, parent_run_id, **kwargs)
        
        if self.current_trace_id:
            # Convert LLMResult to serializable format
            output = {"generations": [[gen.dict() for gen in gens] for gens in response.generations]}
            if response.llm_output:
                output["llm_output"] = response.llm_output
            
            # Include kwargs in metadata
            observation_metadata = {}
            observation_metadata.update({k: v for k, v in kwargs.items() if k not in ["name"]})
                
            observation = ObservationCreate(
                type=ObservationType.LLM,
                name="llm_completion",
                input={},
                output=output,
                tokens=response.llm_output.get("token_usage", {}).get("total_tokens") if response.llm_output and "token_usage" in response.llm_output else None,
                observation_metadata=observation_metadata,
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_llm_error(
        self,
        error: Exception | KeyboardInterrupt,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("LLM error", run_id, parent_run_id, **kwargs)
        
        if self.current_trace_id:
            observation = ObservationCreate(
                type=ObservationType.LLM,
                name="llm_error",
                input={},
                output={"error": str(error)},
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_retriever_end(
        self,
        output: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("Retriever end", run_id, parent_run_id, **kwargs)
        
        if self.current_trace_id:
            # Include kwargs in metadata
            observation_metadata = {}
            observation_metadata.update({k: v for k, v in kwargs.items() if k not in ["name"]})
            
            observation = ObservationCreate(
                type=ObservationType.RETRIEVER,
                name="retriever_end",
                input={},
                output=output,
                observation_metadata=observation_metadata,
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_retriever_start(
        self,
        serialized: dict[str, Any],
        inputs: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("Retriever start", run_id, parent_run_id, **kwargs)
        self._ensure_trace_exists(run_id, parent_run_id, serialized=serialized, inputs=inputs, **kwargs)
        
        if self.current_trace_id:
            # Include serialized and other info in metadata
            observation_metadata = {}
            observation_metadata["serialized"] = serialized
            observation_metadata.update({k: v for k, v in kwargs.items() if k not in ["name"]})
            
            # Ensure inputs is a dictionary - convert it if it's not
            input_dict = {}
            if isinstance(inputs, dict):
                input_dict = inputs
            else:
                # Handle non-dictionary inputs by creating a structured representation
                input_dict = {"raw_input": str(inputs)}
            
            observation = ObservationCreate(
                type=ObservationType.RETRIEVER,
                name=self.get_langchain_run_name(serialized, **kwargs),
                input=input_dict,
                observation_metadata=observation_metadata,
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_retriever_error(
        self,
        error: Exception | KeyboardInterrupt,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        self._log_debug_event("Retriever error", run_id, parent_run_id, **kwargs)
        
        if self.current_trace_id:
            observation = ObservationCreate(
                type=ObservationType.RETRIEVER,
                name="retriever_error",
                input={},
                output={"error": str(error)},
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        self._log_debug_event("Tool start", run_id, parent_run_id, **kwargs)
        self._ensure_trace_exists(run_id, parent_run_id, serialized=serialized, inputs={"input": input_str}, metadata=metadata, **kwargs)
        
        if self.current_trace_id:
            # Include serialized and other info in metadata
            observation_metadata = metadata or {}
            observation_metadata["serialized"] = serialized
            observation_metadata.update({k: v for k, v in kwargs.items() if k not in ["name"]})
            if tags:
                observation_metadata["tags"] = tags
            
            # Ensure input is a dictionary
            input_dict = {"input": str(input_str) if input_str is not None else ""}
            
            observation = ObservationCreate(
                type=ObservationType.TOOL,
                name=self.get_langchain_run_name(serialized, **kwargs),
                input=input_dict,
                observation_metadata=observation_metadata,
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_tool_end(
        self,
        output: dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ):
        self._log_debug_event("Tool end", run_id, parent_run_id, **kwargs)
        
        if self.current_trace_id:
            observation = ObservationCreate(
                type=ObservationType.TOOL,
                name="tool_end",
                input={},
                output=output,
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def on_tool_error(
        self,
        error: Exception | KeyboardInterrupt,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ):
        self._log_debug_event("Tool error", run_id, parent_run_id, **kwargs)
        
        if self.current_trace_id:
            observation = ObservationCreate(
                type=ObservationType.TOOL,
                name="tool_error",
                input={},
                output={"error": str(error)},
                parent_id=str(parent_run_id) if parent_run_id else None,
                run_id=str(run_id)
            )
            self.client.add_observation(self.current_trace_id, observation)

    def get_langchain_run_name(self, seriarized: dict[str, Any], **kwargs: Any) -> str:
        if "name" in kwargs and kwargs["name"] is not None:
            return kwargs["name"]

        if "name" in seriarized:
            return seriarized["name"]

        return "<unknown>"

    def _ensure_trace_exists(
        self,
        run_id: UUID | None,
        parent_run_id: UUID | None = None,
        serialized: dict[str, Any] = None,
        inputs: dict[str, Any] | Any = None,
        metadata: dict[str, Any] = None,
        **kwargs: Any,
    ):
        """Ensure that a trace exists for the current run."""
        if self.current_trace_id is not None:
            return
        
        # Only create a trace for the root run (no parent_run_id)
        if parent_run_id is None and run_id is not None:
            # Extract user query from inputs
            user_query = ""
            if inputs:
                # Convert inputs to dict if it's not already
                input_dict = {}
                if isinstance(inputs, dict):
                    input_dict = inputs
                    # Try to find a query in the inputs
                    if "query" in input_dict:
                        user_query = input_dict["query"]
                    elif "input" in input_dict and isinstance(input_dict["input"], str):
                        user_query = input_dict["input"]
                    elif "messages" in input_dict and input_dict["messages"]:
                        # Try to extract from chat messages
                        for msg in input_dict["messages"]:
                            if isinstance(msg, dict) and msg.get("type") in ["human", "user"] and "content" in msg:
                                user_query = msg["content"]
                                break
                else:
                    # Try to get meaningful content from non-dict inputs
                    try:
                        if hasattr(inputs, "content"):
                            # Handle message objects that might have content attribute
                            user_query = str(inputs.content)
                        elif isinstance(inputs, list) and inputs and hasattr(inputs[0], "content"):
                            # Handle list of message objects
                            user_query = str(inputs[0].content)
                        else:
                            # Default fallback
                            user_query = str(inputs)
                    except:
                        user_query = str(inputs)
            
            # Create a new trace
            trace_data = TraceCreate(
                user_query=user_query,
                trace_metadata=metadata or self.metadata
            )
            
            try:
                self.current_trace_id = self.client.create_trace(trace_data)
                self.log.debug(f"Created new trace with ID: {self.current_trace_id}")
                
                if run_id:
                    self.runs[run_id] = self.current_trace_id
            except Exception as e:
                self.log.error(f"Failed to create trace: {e}")

    def _log_debug_event(
        self, event_name: str, run_id: UUID, parent_run_id: UUID | None = None, **kwargs
    ) -> None:
        self.log.debug(
            f"{event_name} run_id={str(run_id)} parent_run_id={str(parent_run_id)}"
        )
