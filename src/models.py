from pydantic import BaseModel
from typing import Any, Dict, List


class FunctionProperty(BaseModel):
    type: str
    description: str | None = None


class FunctionParameters(BaseModel):
    type: str
    properties: Dict[str, FunctionProperty]
    required: List[str]


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters
    returns: Dict[str, str] | None = None


class PromptTest(BaseModel):
    prompt: str


class FunctionsCallResult(BaseModel):
    prompt: str
    name: str
    parameters: Dict[str, Any]
