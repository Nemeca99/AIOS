# fragments.py
import uuid
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Fragment:
    id: str
    content: str
    size: int
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    hits: int = 0
    last_access: float = field(default_factory=time.time)
    level: int = 0
    tags: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None

def make_fragment(content: str, parent: Optional[str]=None, level:int=0, tags=None):
    return Fragment(
        id=f"root_{uuid.uuid4().hex[:8]}",
        content=content,
        size=len(content.encode('utf-8')),
        parent=parent,
        children=[],
        hits=0,
        level=level,
        tags=tags or []
    )
