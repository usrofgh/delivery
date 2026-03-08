from pydantic import BaseModel, Field


class RegisterCustomerSchema(BaseModel):
    name: str = Field(min_length=1, max_length=300, examples=["John", "John Snow"])
    email: str = Field(max_length=500, examples=["johnshow@gmail.com"])
    password: str = Field(min_length=8, max_length=5000, examples=["stringst"])


class RegisterCustomerResponseSchema(BaseModel):
    message: str = "INSTRUCTIONS_SENT_ON_EMAIL"


class RegisterCustomerConfirmSchema(BaseModel):
    pass
