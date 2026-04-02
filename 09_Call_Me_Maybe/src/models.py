from pydantic import BaseModel, Field
from typing import Any, Dict


class ParameterSchema(BaseModel):
    """Schema for a single function parameter"""
    type: str = Field(min_length=1)


class FunctionDefinition(BaseModel):
    """Definition of a callable function"""
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    parameters: Dict[str, ParameterSchema]
    returns: Dict[str, Any]


class TestPrompt(BaseModel):
    """A single natural language test prompt"""
    prompt: str


class FunctionCall(BaseModel):
    """A generated function call result"""
    prompt: str
    name: str
    parameters: Dict[str, Any]
