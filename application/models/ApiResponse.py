from pydantic import BaseModel
from typing import Optional

class ApiResponse(BaseModel):
    status: int
    data: Optional[dict] | None
    error: bool
    
