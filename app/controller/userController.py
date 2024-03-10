from app.database import get_db
from app.model.requestModel import UserInfo
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session



router = APIRouter()


@router.post("/signUp")
async def userSignup(request:Request, payload:UserInfo, dbConn:Session()=Depends(get_db)): # type: ignore
    pass


@router.post("/login")
async def userLogin(request:Request, payload:UserInfo, dbConn:Session()=Depends(get_db)): # type: ignore
    pass