from pydantic import BaseModel, EmailStr, field_validator, model_validator

class UserCreate(BaseModel):
    email: EmailStr # valid email address format (e.g. name@example.com)
    username: str
    password: str
    confirm_password: str

    # validates username
    # note - cls = class, v = username value
    @field_validator("username")
    @classmethod
    def username_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Username cannot be empty")
        return v

    # validate that both password and confirm password matches
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self