from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# from search.schemas import SearchResponseSchema
from typing import Union


class SearchResponseSchema(BaseModel):
    is_vip: bool
    name: str
    gender: Optional[str] = None
    occupation: Optional[str] = None
    age: Optional[int] = None


class HistoryBase(BaseModel):
    input: str
    result: Optional[SearchResponseSchema] = None

    class Config:
        orm_mode = True


class CreateHistory(HistoryBase):
    user_id: Optional[int]

class GetHistory(HistoryBase):
    id: int
    created_at: datetime