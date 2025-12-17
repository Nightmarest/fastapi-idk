from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserUpdate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class CasinoCreate(BaseModel):
    name: str


class CasinoResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class ReviewCreate(BaseModel):
    stars: int = Field(..., ge=1, le=5)
    comment: str
    casino_id: int


class ReviewResponse(BaseModel):
    id: int
    stars: int
    comment: str
    user_id: int
    casino_id: int

    model_config = {"from_attributes": True}
