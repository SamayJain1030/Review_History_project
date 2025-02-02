from pydantic import BaseModel

class AccessLog(BaseModel):
    endpoint: str
    timestamp: str

    class Config():
        orm_mode =  True 