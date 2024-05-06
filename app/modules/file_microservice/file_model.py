from pydantic import BaseModel

class File(BaseModel):
    file_name: str
    file_type: str
    file_size: int
    user_id: int
