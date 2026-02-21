from pydantic import BaseModel
from typing import List

class AutomixRequest(BaseModel):
    track_ids: List[str]
    auto_order: bool = True
    mode: str = "smooth"