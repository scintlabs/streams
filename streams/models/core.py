from __future__ import annotations
from attrs import define, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

@define
class Provider:
    id: UUID = field(factory=uuid4)
    name: str = field()
    created: datetime = field(factory=datetime.utcnow)

@define
class Stream:
    id: UUID = field(factory=uuid4)
    provider_id: UUID = field()
    name: str = field()
    created: datetime = field(factory=datetime.utcnow)

@define
class Message:
    id: UUID = field(factory=uuid4)
    stream_id: UUID = field()
    author: str = field()
    content: str = field()
    ts: datetime = field(factory=datetime.utcnow)
    epoch_id: Optional[str] = field(default=None)
