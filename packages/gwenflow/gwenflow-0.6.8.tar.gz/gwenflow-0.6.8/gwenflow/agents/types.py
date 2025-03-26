
import uuid
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator, UUID4
from time import time


class AgentResponse(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4, frozen=True)
    content: Optional[str] = ""
    thinking: Optional[str] = ""
    created_at: int = Field(default_factory=lambda: int(time()))
    finish_reason: Optional[str] = None

    @field_validator("id", mode="before")
    @classmethod
    def deny_user_set_id(cls, v: Optional[UUID4]) -> None:
        if v:
            raise ValueError("This field is not to be set by the user.")
