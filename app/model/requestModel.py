from pydantic import BaseModel, Field, field_validator
import re



class Address(BaseModel):
    longitude  : float = Field(le=180,ge=-180)
    latitude   : float = Field(le=90,ge=-90)


class GetAddressesWithDistance(BaseModel):
    longitude  : float = Field(le=180,ge=-180)
    latitude   : float = Field(le=90,ge=-90)
    distance    : int = Field(strict=True)

    



class UserInfo(BaseModel):
    emailId  : str
    password : str

    @field_validator("password", mode="after")
    def passwordValidator(cls, value)-> str:
        passwordPatter = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:\"<>?`\-=[\];',.\/])(?!.*\s).{8,}$")
        if not passwordPatter.match(value):
            raise ValueError("Password should be greater than 8 digit and should contian special character, digit and upper letter")
        else:
            return value
        

    @field_validator("emailId", mode="after")
    def emailValidator(cls, value)-> str:
        emailPattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if not emailPattern.match(value):
            raise ValueError("Invalid email Id")
        else:
            return value