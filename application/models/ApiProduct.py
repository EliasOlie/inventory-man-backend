from pydantic import BaseModel
from typing import Optional

class ApiProduct(BaseModel):
    name: str
    price: float
    amount: int
    description: Optional[str]

class ProductOperation(BaseModel):
    id: Optional[str]
    field: Optional[str]
    value: Optional[str]
