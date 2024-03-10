from pydantic import BaseModel, Field, field_validator
import re



class Address(BaseModel):
    emailId : str
    latitude : str  = Field(pattern='^(-?\d{1,2}(?:\.\d{1,6})?|-?90(?:\.0{1,6})?)$')
    longitude : str = Field(pattern='^(-?\d{1,3}(?:\.\d{1,6})?|-?180(?:\.0{1,6})?)$')


class GetAddressesWithDistance(BaseModel):
    latitude : str  = Field(pattern='^(-?\d{1,2}(?:\.\d{1,6})?|-?90(?:\.0{1,6})?)$')
    longitude : str = Field(pattern='^(-?\d{1,3}(?:\.\d{1,6})?|-?180(?:\.0{1,6})?)$')
    distance : int  = Field(strict=True)

    



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