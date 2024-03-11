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
    """
    Endpoint to add a new user address.

    Args:
        request: FastAPI Request object.
        payload: Address model representing the new address data.
        dbConn: Database session dependency.

    Returns:
        Response with information about the added address.
    """
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    payload = jsonable_encoder(payload)
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))
    return await addUserAddressInfoToDb(requestId, dbConn, loggedInUserInfo, payload)



@router.get("/fetchUserAddress")
async def addUserAddress(request:Request, dbConn:Session()=Depends(get_db)): # type: ignore
    """
    Endpoint to fetch user's address information.

    Args:
        request: FastAPI Request object.
        dbConn: Database session dependency.

    Returns:
        Response with user's address information.
    """
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))
    return await getuserAddressInfoFromDb(requestId, dbConn, loggedInUserInfo)


@router.patch("/updateAddress")
async def addUserAddress(request:Request, payload:Address, dbConn:Session()=Depends(get_db)): # type: ignore
    """
    Endpoint to update an existing user address.

    Args:
        request: FastAPI Request object.
        payload: Address model representing the updated address data.
        dbConn: Database session dependency.

    Returns:
        Response with information about the updated address.
    """
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    payload = jsonable_encoder(payload)
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))
    return await updateUserAddressInfoToDb(requestId=requestId, dbConn=dbConn, loggedInUserInfo=loggedInUserInfo, payload=payload)


@router.post("/addressWithInDistance")
async def fetchAllAddressWithPerimeter(request:Request, payload:GetAddressesWithDistance, dbConn:Session()=Depends(get_db)): # type: ignore
    """
    Endpoint to fetch all addresses within a given distance from a specified point.

    Args:
        request: FastAPI Request object.
        payload: GetAddressesWithDistance model representing the search criteria.
        dbConn: Database session dependency.

    Returns:
        Response with addresses within the specified distance.
    """

    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    payload = jsonable_encoder(payload)
    loggedInUserInfo = await getCurrentUserInfo(dbConn, request.headers.get("authorization"))
    return await getAllAddressWithInPerimeterFromDb(requestId=requestId, dbConn=dbConn, payload=payload)