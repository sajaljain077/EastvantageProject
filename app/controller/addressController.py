from app.database import get_db
from app.model.requestModel import GetAddressesWithDistance, Address
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.utils.auth import getCurrentUserInfo



router = APIRouter()


@router.post("/addAddress")
async def addUserAddress(request:Request, payload:Address, dbConn:Session()=Depends(get_db)): # type: ignore
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))


@router.get("/fetchAddress")
async def addUserAddress(request:Request, emailId: str, dbConn:Session()=Depends(get_db)): # type: ignore
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))


@router.patch("/fetchAddress")
async def addUserAddress(request:Request, payload:Address, dbConn:Session()=Depends(get_db)): # type: ignore
    pass