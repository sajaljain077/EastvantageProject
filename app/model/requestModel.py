from pydantic import BaseModel, Field



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


