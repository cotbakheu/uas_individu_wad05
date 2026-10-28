from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def validate_bcrypt_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password cannot exceed 72 UTF-8 bytes")
    return password


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    _validate_password = field_validator("password")(validate_bcrypt_password)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    _validate_password = field_validator("password")(validate_bcrypt_password)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: str


class AuthResponse(BaseModel):
    user: UserResponse
    csrf_token: str
