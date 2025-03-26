import requests
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from datetime import datetime
from uuid import UUID
import json
from pydantic import BaseModel, Field


class ObservationType(str, Enum):
    """Type of observation in a trace."""
    LLM = "LLM"
    RETRIEVER = "RETRIEVER"
    TOOL = "TOOL"
    OTHER = "OTHER"


class TraceStatus(str, Enum):
    """Status of a trace."""
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class TraceCreate(BaseModel):
    """Data required to create a new trace."""
    user_query: str
    trace_metadata: Optional[Dict[str, Any]] = None


class TraceUpdate(BaseModel):
    """Data for updating a trace."""
    final_response: Optional[str] = None
    status: Optional[TraceStatus] = None
    trace_metadata: Optional[Dict[str, Any]] = None
    latency_ms: Optional[int] = None
    total_tokens: Optional[int] = None
    cost: Optional[float] = None


class ObservationCreate(BaseModel):
    """Data required to create a new observation."""
    type: ObservationType
    name: str
    input: Dict[str, Any]
    output: Optional[Dict[str, Any]] = None
    latency_ms: Optional[int] = None
    tokens: Optional[int] = None
    cost: Optional[float] = None
    observation_metadata: Optional[Dict[str, Any]] = None
    parent_id: Optional[Union[UUID, str]] = None
    trace_id: Optional[Union[UUID, str]] = None
    run_id: Optional[str] = None


class DatagustoClient:
    """
    Client for interacting with the Datagusto API.
    """
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the Datagusto client.
        
        Args:
            base_url: The base URL of the Datagusto API
            api_key: The API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def create_trace(self, trace_data: Union[TraceCreate, Dict[str, Any]]) -> str:
        """
        Create a new trace.
        
        Args:
            trace_data: The trace data or TraceCreate object
            
        Returns:
            The trace ID
        
        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        url = f"{self.base_url}/api/v1/sdk/traces"
        
        # Convert to dict if it's a Pydantic model
        try:
            if isinstance(trace_data, BaseModel):
                # For Pydantic v2
                if hasattr(trace_data, "model_dump"):
                    data = trace_data.model_dump()
                # For Pydantic v1 backward compatibility  
                elif hasattr(trace_data, "dict"):
                    data = trace_data.dict()
                else:
                    data = dict(trace_data.__dict__)
            else:
                data = trace_data
        except Exception as e:
            # Fallback method
            data = trace_data
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json().get("trace_id")
    
    def add_observation(self, trace_id: Union[UUID, str], observation_data: Union[ObservationCreate, Dict[str, Any]]) -> str:
        """
        Add an observation to a trace.
        
        Args:
            trace_id: The ID of the trace
            observation_data: The observation data or ObservationCreate object
            
        Returns:
            The observation ID
        
        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        url = f"{self.base_url}/api/v1/sdk/observations"
        
        # Convert to dict if it's a Pydantic model
        try:
            if isinstance(observation_data, BaseModel):
                # For Pydantic v2
                if hasattr(observation_data, "model_dump"):
                    data = observation_data.model_dump()
                # For Pydantic v1 backward compatibility
                elif hasattr(observation_data, "dict"):
                    data = observation_data.dict()
                else:
                    data = dict(observation_data.__dict__)
            else:
                data = dict(observation_data)
        except Exception as e:
            # Fallback method
            data = dict(observation_data)
        
        # Ensure trace_id is properly formatted as a string UUID
        trace_id_str = str(trace_id) if isinstance(trace_id, UUID) else trace_id
        data["trace_id"] = trace_id_str
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json().get("observation_id")
    
    def complete_trace(self, trace_id: Union[UUID, str], completion_data: Optional[Union[TraceUpdate, Dict[str, Any]]] = None) -> bool:
        """
        Mark a trace as completed.
        
        Args:
            trace_id: The ID of the trace
            completion_data: Optional additional data for completion or TraceUpdate object
            
        Returns:
            True if successful
        
        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        trace_id_str = str(trace_id) if isinstance(trace_id, UUID) else trace_id
        url = f"{self.base_url}/api/v1/sdk/traces/{trace_id_str}/complete"
        
        if completion_data is None:
            data = {}
        else:
            try:
                if isinstance(completion_data, BaseModel):
                    # For Pydantic v2
                    if hasattr(completion_data, "model_dump"):
                        data = completion_data.model_dump()
                    # For Pydantic v1 backward compatibility
                    elif hasattr(completion_data, "dict"):
                        data = completion_data.dict()
                    else:
                        data = dict(completion_data.__dict__)
                else:
                    data = completion_data
            except Exception as e:
                # Fallback method
                data = completion_data
        
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json().get("success", False)
