from pydantic import BaseModel

class Medicine(BaseModel):
    name: str
    salt: str
    symptom: str

    class Config:
        orm_mode = True