from app.database import get_db
from app.model.requestModel import GetAddressesWithDistance, Address
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.utils.auth import getCurrentUserInfo
from app.service.crudOperation import getuserAddressInfoFromDb, addUserAddressInfoToDb, updateUserAddressInfoToDb, getAllAddressWithInPerimeterFromDb
import uuid
from fastapi.encoders import jsonable_encoder



router = APIRouter()


@router.post("/addAddress")
async def addUserAddress(request:Request, payload:Address, dbConn:Session()=Depends(get_db)): # type: ignore
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    payload = jsonable_encoder(payload)
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))
    return await addUserAddressInfoToDb(requestId, dbConn, loggedInUserInfo, payload)



@router.get("/fetchUserAddress")
async def addUserAddress(request:Request, dbConn:Session()=Depends(get_db)): # type: ignore
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))
    return await getuserAddressInfoFromDb(requestId, dbConn, loggedInUserInfo)


@router.patch("/updateAddress")
async def addUserAddress(request:Request, payload:Address, dbConn:Session()=Depends(get_db)): # type: ignore
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    payload = jsonable_encoder(payload)
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))
    return await updateUserAddressInfoToDb(requestId=requestId, dbConn=dbConn, loggedInUserInfo=loggedInUserInfo, payload=payload)


@router.post("/addressWithInDistance")
async def fetchAllAddressWithPerimeter(request:Request, payload:GetAddressesWithDistance, dbConn:Session()=Depends(get_db)): # type: ignore
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    payload = jsonable_encoder(payload)
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))
    return await getAllAddressWithInPerimeterFromDb(requestId=requestId, dbConn=dbConn, loggedInUserInfo=loggedInUserInfo, payload=payload)