from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import uuid4
from datetime import datetime

class MemoryNode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    type: str
    importance: float = Field(default=0.5)
    emotion_context: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    # --- NÂNG CẤP: Cho ReasonMap ---
    parent_id: Optional[str] = None 
    reason: Optional[str] = None
