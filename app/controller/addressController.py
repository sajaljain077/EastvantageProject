from app.database import get_db
from app.model.requestModel import GetAddressesWithDistance, Address
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session



router = APIRouter()


@router.post("/addAddress")
async def addUserAddress(request:Request, payload:Address, dbConn:Session()=Depends(get_db)): # type: ignore
    pass


@router.get("/fetchAddress")
async def addUserAddress(request:Request, emailid: str, dbConn:Session()=Depends(get_db)): # type: ignore
    pass


@router.patch("/fetchAddress")
async def addUserAddress(request:Request, payload:Address, dbConn:Session()=Depends(get_db)): # type: ignore
    pass