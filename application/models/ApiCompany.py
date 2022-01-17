from pydantic import BaseModel
from typing import Optional

class ApiCompany(BaseModel):
    name: str
    email: str
    cnpj: str
    address: Optional[str]
    
class CompanyOperation(BaseModel):
    field: str
    value: str