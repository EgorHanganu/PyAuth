from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    username: constr(min_length=6, max_length=20, pattern=r'^\w+$') # type: ignore
    password: constr(min_length=6, max_length=20) # type: ignore

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
