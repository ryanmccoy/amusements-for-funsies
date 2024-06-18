from pydantic import BaseModel
from typing import List

class ErrorItem(BaseModel):
    status: str
    title: str

class Validator(BaseModel):
    errors: List[ErrorItem]