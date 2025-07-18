from pydantic import BaseModel, Field
from typing import Dict, Any
from uuid import uuid4
from datetime import datetime

class ThoughtChunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    origin: str  # e.g., "cortex", "autobot", "memory"
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
