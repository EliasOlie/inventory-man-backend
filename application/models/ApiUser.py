from pydantic import BaseModel
from typing import Any, Optional

class ApiUser(BaseModel):
    name: str
    email: str
    company: str
    password: str
    role: Optional[str]
    
class UserOperation(BaseModel):
    field: str
    value: str
    user_external: Optional[str]
    extra: Optional[Any]
    
class UserOp(BaseModel):
    id: Optional[str]
    field: Optional[str]
    value: Optional[str]