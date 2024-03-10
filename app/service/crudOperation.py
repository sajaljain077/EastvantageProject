from app.schema import Users, Address
from app.utils.utis import errorMaker, responseMaker, hashValueGenerator
from app.constant import SECRETKEY
from datetime import datetime
from datetime import datetime, timedelta, timezone
from app.utils.auth import create_access_token
from fastapi.encoders import jsonable_encoder
from app.constant import ACCESS_TOKEN_EXPIRE_MINUTES





async def addUserToDb(dbConn, payload, requestId):
    emailId = payload.get("emailId")
    if dbConn.query(Users).filter(Users.emailId == emailId).first():
        return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("emailAlreadyExist", emailId)])
    try:
        dbresp = Users(emailId = emailId, hashedPassword = await hashValueGenerator(payload.get("password"), SECRETKEY), createdOn = datetime.now())
        dbConn.add(dbresp)
        dbConn.commit()
    except Exception as err:
        return await responseMaker(statusCode=500, requestId=requestId, errors=[], data={"msg":"Internal Service Error"})
    return await responseMaker(statusCode=200, requestId=requestId, errors=[], data={"msg":"User Registerd Successfully, please login"})



async def checkUserExist(dbConn, payload, requestId):
    emailId = payload.get("emailId")
    password = payload.get("password")
    if not dbConn.query(Users).filter(Users.emailId == emailId).first():
        return await responseMaker(statusCode=401, data={}, requestId=requestId, errors=[await errorMaker("userIsNotSignedup")])
    userInfo = dbConn.query(Users).filter(Users.emailId == emailId, Users.hashedPassword == await hashValueGenerator(password, seceretKey=SECRETKEY)).first()
    if not userInfo:
        return await responseMaker(401, data={}, requestId=requestId, errors=[errorMaker("unauthorizedUser")])
    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = await create_access_token(data={"sub": payload["emailId"]}, expires_delta=accessTokenExpires)
    return await responseMaker(statusCode=200, requestId=requestId, data={"accessToken":accessToken})


async def getuserAddressInfoFromDb(requestId, dbConn, userInfo):
    try:
        addressInfo = jsonable_encoder(dbConn.query(Address).filter(Address.userId == userInfo["id"]).all())
    except Exception as err:
        return await responseMaker(statusCode=500, requestId=requestId, errors=[], data={"msg":"Internal Service Error"})
    return await responseMaker(statusCode=200, requestId=requestId, data=addressInfo)


async def addUserAddressInfoToDb(requestId, dbConn, loggedInUserInfo, payload):
    if not dbConn.query(Address).filter(Address.userId == loggedInUserInfo.get("id")).first():
        addresp = Address(userId = loggedInUserInfo["id"], latitude = payload.get("latitude"), longitude = payload.get("longitude"), createdOn = datetime.now())
        try:
            dbConn.add(addresp)
            dbConn.commit()
        except Exception as err:
            return await responseMaker(statusCode=500, requestId=requestId, errors=[], data={"msg":"Internal Service Error"})
        return await responseMaker(statusCode=200, requestId=requestId, data={"msg":"User address added succeessfully"})
    return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("addressAlreadyExist")])


async def updateUserAddressInfoToDb(requestId, dbConn, loggedInUserInfo, payload):
    addressInfo = dbConn.query(Address).filter(Address.userId == loggedInUserInfo.get("id"))
    if addressInfo.first():
        try:
            addressInfo.update({"latitude": payload.get("latitude"), "longitude" : payload.get("longitude"), "updatedon":datetime.now()})
            dbConn.commit()
        except Exception as err:
            return await responseMaker(statusCode=500, requestId=requestId, errors=[], data={"msg":"Internal Service Error"})
        return await responseMaker(statusCode=200, requestId=requestId, data={"msg":"User address edited succeessfully"})
    return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("addressDoesNotExist")])



async def getAllAddressWithInPerimeterFromDb(requestId, dbConn, loggedInUserInfo, payload):
    pass