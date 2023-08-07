from pydantic import BaseModel

class MessageClass(BaseModel):
    user_id: str
    current_user: str
    message: str
    transaction_id: int