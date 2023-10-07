from pydantic import BaseModel

class MessageClass(BaseModel):
    sender_id: str
    reciever_id: str