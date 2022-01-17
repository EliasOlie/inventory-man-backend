from pydantic import BaseModel

class Auth(BaseModel):
    username: str
    password: str

class AuthRes(BaseModel):
    user_id: str
    user_company: str
    user_role: str
    is_active: bool
    
class AuthResFail(BaseModel):
    status:int
    data: dict
    error: bool