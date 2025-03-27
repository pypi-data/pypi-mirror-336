from pydantic import BaseModel, Field
from typing import Literal, List, Union, Optional


class Statement(BaseModel):
    effect: Literal["allow", "deny"]
    action: Union[str, List[str]]
    resource: Union[str, List[str]]
    condition: Optional[dict] = None


class PolicyDocument(BaseModel):
    version: str = Field(default="2025-03-26")
    statement: List[Statement]
