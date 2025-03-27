import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Response:
    # task specific items
    id: int
    start: float
    end: Optional[float] = None

    # aio response specific items
    content: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    status: Optional[int] = None
    headers: Optional[dict] = None

    def json(self):
        try:
            return json.loads(self.content)
        except (json.JSONDecodeError, TypeError):
            raise

    def __repr__(self):
        return f"{self.status}"
