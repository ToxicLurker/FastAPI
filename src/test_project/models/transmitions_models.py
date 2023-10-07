from pydantic import BaseModel
from typing import Optional

class MessageClass(BaseModel):
    user_id: str
    current_user: str
    message: str
    transaction_id: Optional[int]

class MessageClassNew(BaseModel):
    user_id: str
    current_user: str
    message: str