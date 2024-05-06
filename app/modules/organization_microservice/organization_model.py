from pydantic import BaseModel

class Organization(BaseModel):
    organization_name: str
