"""
Classes for representing examples in a dataset.
"""


from typing import Optional, Any, Dict, List, Union
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from datetime import datetime
import time


class ExampleParams(Enum):
    INPUT = "input"
    ACTUAL_OUTPUT = "actual_output"
    EXPECTED_OUTPUT = "expected_output"
    CONTEXT = "context"
    RETRIEVAL_CONTEXT = "retrieval_context"
    TOOLS_CALLED = "tools_called"
    EXPECTED_TOOLS = "expected_tools"
    REASONING = "reasoning"
    ADDITIONAL_METADATA = "additional_metadata"


class Example(BaseModel):
    input: Optional[str] = None
    actual_output: Optional[Union[str, List[str]]] = None
    expected_output: Optional[Union[str, List[str]]] = None
    context: Optional[List[str]] = None
    retrieval_context: Optional[List[str]] = None
    additional_metadata: Optional[Dict[str, Any]] = None
    tools_called: Optional[List[str]] = None
    expected_tools: Optional[List[str]] = None
    name: Optional[str] = None
    example_id: str = Field(default_factory=lambda: str(uuid4()))
    example_index: Optional[int] = None
    timestamp: Optional[str] = None
    trace_id: Optional[str] = None
    
    def __init__(self, **data):
        if 'example_id' not in data:
            data['example_id'] = str(uuid4())
        # Set timestamp if not provided
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().strftime("%Y%m%d_%H%M%S")
        super().__init__(**data)
    
    @field_validator('input', mode='before')
    @classmethod
    def validate_input(cls, v):
        if v is not None and (not v or not isinstance(v, str)):
            raise ValueError(f"Input must be a non-empty string but got '{v}' of type {type(v)}")
        return v
    
    @field_validator('actual_output', mode='before')
    @classmethod
    def validate_actual_output(cls, v):
        if v is not None:
            if not isinstance(v, (str, list)):
                raise ValueError(f"Actual output must be a string or a list of strings but got {v} of type {type(v)}")
            if isinstance(v, list) and not all(isinstance(item, str) for item in v):
                raise ValueError(f"All items in actual_output must be strings but got {v}")
        return v
    
    @field_validator('expected_output', mode='before')
    @classmethod
    def validate_expected_output(cls, v):
        if v is not None and not isinstance(v, (str, list)):
            raise ValueError(f"Expected output must be a string, a list of strings, or None but got {v} of type {type(v)}")
        if isinstance(v, list) and not all(isinstance(item, str) for item in v):
            raise ValueError(f"All items in expected_output must be strings but got {v}")
        return v
    
    @field_validator('context', 'retrieval_context', 'tools_called', 'expected_tools', mode='before')
    @classmethod
    def validate_string_lists(cls, v, info):
        field_name = info.field_name
        if v is not None:
            if not isinstance(v, list):
                raise ValueError(f"{field_name} must be a list of strings or None but got {v} of type {type(v)}")
            for i, item in enumerate(v):
                if not isinstance(item, str):
                    raise ValueError(f"All items in {field_name} must be strings but item at index {i} is {item} of type {type(item)}")
        return v
    
    @field_validator('additional_metadata', mode='before')
    @classmethod
    def validate_additional_metadata(cls, v):
        if v is not None and not isinstance(v, dict):
            raise ValueError(f"Additional metadata must be a dictionary or None but got {v} of type {type(v)}")
        return v
    
    @field_validator('example_index', mode='before')
    @classmethod
    def validate_example_index(cls, v):
        if v is not None and not isinstance(v, int):
            raise ValueError(f"Example index must be an integer or None but got {v} of type {type(v)}")
        return v
    
    @field_validator('timestamp', mode='before')
    @classmethod
    def validate_timestamp(cls, v):
        if v is not None and not isinstance(v, str):
            raise ValueError(f"Timestamp must be a string or None but got {v} of type {type(v)}")
        return v
    
    @field_validator('trace_id', mode='before')
    @classmethod
    def validate_trace_id(cls, v):
        if v is not None and not isinstance(v, str):
            raise ValueError(f"Trace ID must be a string or None but got {v} of type {type(v)}")
        return v

    def to_dict(self):
        return {
            "input": self.input,
            "actual_output": self.actual_output,
            "expected_output": self.expected_output,
            "context": self.context,
            "retrieval_context": self.retrieval_context,
            "additional_metadata": self.additional_metadata,
            "tools_called": self.tools_called,
            "expected_tools": self.expected_tools,
            "name": self.name,
            "example_id": self.example_id,
            "example_index": self.example_index,
            "timestamp": self.timestamp,
            "trace_id": self.trace_id
        }

    def __str__(self):
        return (
            f"Example(input={self.input}, "
            f"actual_output={self.actual_output}, "
            f"expected_output={self.expected_output}, "
            f"context={self.context}, "
            f"retrieval_context={self.retrieval_context}, "
            f"additional_metadata={self.additional_metadata}, "
            f"tools_called={self.tools_called}, "
            f"expected_tools={self.expected_tools}, "
            f"name={self.name}, "
            f"example_id={self.example_id}, "
            f"example_index={self.example_index}, "
            f"timestamp={self.timestamp}, "
            f"trace_id={self.trace_id})"
        )
