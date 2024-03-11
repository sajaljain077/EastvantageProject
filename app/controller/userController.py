from app.database import get_db
from app.model.requestModel import UserInfo
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.service.crudOperation import addUserToDb, checkUserExist
import uuid
import sys
from app.utils.log import logger

router = APIRouter()


@router.post("/signUp")
async def userSignup(request:Request, payload:UserInfo, dbConn:Session()=Depends(get_db)): # type: ignore
    """
    Endpoint for user signup.

    Args:
        request: FastAPI Request object.
        payload: UserInfo model representing user signup data.
        dbConn: Database session dependency.    

    Returns:
        Response with information about the signup status.
    """
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    payload = jsonable_encoder(payload)
    response = await addUserToDb(dbConn, payload, requestId)
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return response



@router.post("/login")
async def userLogin(request:Request, payload:UserInfo, dbConn:Session()=Depends(get_db), ): # type: ignore
    """
    Endpoint for user login.

    Args:
        request: FastAPI Request object.
        payload: UserInfo model representing user login data.
        dbConn: Database session dependency.

    Returns:
        Response with information about the login status.
    """
    requestId = request.headers.get("requestId", str(uuid.uuid4()))
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    payload = jsonable_encoder(payload)
    response = await checkUserExist(dbConn, payload, requestId)
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    return response