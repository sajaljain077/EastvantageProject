from app.schema import Users, Address
from app.utils.utis import errorMaker, responseMaker, hashValueGenerator
from app.constant import SECRETKEY
from datetime import datetime
from datetime import datetime, timedelta, timezone
from app.utils.auth import create_access_token
from fastapi.encoders import jsonable_encoder
from app.constant import ACCESS_TOKEN_EXPIRE_MINUTES
import math
import sys
from app.utils.log import logger





async def addUserToDb(dbConn, payload, requestId):
    """
        Function to check whether log in user is valid or not
        Args:
            requestid, db connection, payload

        Returns:
            Access Token
    """
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    emailId = payload.get("emailId")
    if dbConn.query(Users).filter(Users.emailId == emailId).first():
        return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("emailAlreadyExist", emailId)])
    try:
        dbresp = Users(emailId = emailId, hashedPassword = await hashValueGenerator(payload.get("password"), SECRETKEY), createdOn = datetime.now())
        dbConn.add(dbresp)
        dbConn.commit()
    except Exception as err:
        logger.error('{} {}'.format(requestId, f"got following error - {err}"), exc_info=True)
        return await responseMaker(statusCode=500, requestId=requestId, errors=[], data={"msg":"Internal Service Error"})
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return await responseMaker(statusCode=200, requestId=requestId, errors=[], data={"msg":"User Registerd Successfully, please login"})



async def checkUserExist(dbConn, payload, requestId):
    """
        Function to check whether log in user is valid or not
        Args:
            requestid, db connection, payload

        Returns:
            Access Token
    """
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    emailId = payload.get("emailId")
    password = payload.get("password")
    if not dbConn.query(Users).filter(Users.emailId == emailId).first():
        return await responseMaker(statusCode=401, data={}, requestId=requestId, errors=[await errorMaker("userIsNotSignedup")])
    userInfo = dbConn.query(Users).filter(Users.emailId == emailId, Users.hashedPassword == await hashValueGenerator(password, seceretKey=SECRETKEY)).first()
    if not userInfo:
        return await responseMaker(401, data={}, requestId=requestId, errors=[errorMaker("unauthorizedUser")])
    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = await create_access_token(data={"sub": payload["emailId"]}, expires_delta=accessTokenExpires)
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return await responseMaker(statusCode=200, requestId=requestId, data={"accessToken":accessToken})


async def getuserAddressInfoFromDb(requestId, dbConn, userInfo):
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    try:
        addressInfo = jsonable_encoder(dbConn.query(Address).filter(Address.userId == userInfo["id"]).all())
    except Exception as err:
        logger.error('{} {}'.format(requestId, f"got following error - {err}"), exc_info=True)
        return await responseMaker(statusCode=500, requestId=requestId, errors=[], data={"msg":"Internal Service Error"})
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return await responseMaker(statusCode=200, requestId=requestId, data=addressInfo)


async def addUserAddressInfoToDb(requestId, dbConn, loggedInUserInfo, payload):
    """
    Function to add the user address
    Args:
        requestid, db connection, user info whose data need to be added, payload

    Returns:
        Successfull message
    """
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    if not dbConn.query(Address).filter(Address.userId == loggedInUserInfo.get("id")).first():
        addresp = Address(userId = loggedInUserInfo["id"], latitude = payload.get("latitude"), longitude = payload.get("longitude"), createdOn = datetime.now())
        try:
            dbConn.add(addresp)
            dbConn.commit()
        except Exception as err:
            logger.error('{} {}'.format(requestId, f"got following error - {err}"), exc_info=True)
            return await responseMaker(statusCode=500, requestId=requestId, errors=[], data={"msg":"Internal Service Error"})
        logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
        return await responseMaker(statusCode=200, requestId=requestId, data={"msg":"User address added succeessfully"})
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("addressAlreadyExist")])


async def updateUserAddressInfoToDb(requestId, dbConn, loggedInUserInfo, payload):
    """
    Function to update the user address
    Args:
        requestid, db connection, user info whose data need to be updated, payload

    Returns:
        Successful message
    """
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    addressInfo = dbConn.query(Address).filter(Address.userId == loggedInUserInfo.get("id"))
    if addressInfo.first():
        try:
            addressInfo.update({"latitude": payload.get("latitude"), "longitude" : payload.get("longitude"), "updatedon":datetime.now()})
            dbConn.commit()
        except Exception as err:
            logger.error('{} {}'.format(requestId, f"got following error - {err}"), exc_info=True)
            return await responseMaker(statusCode=500, requestId=requestId, errors=[], data={"msg":"Internal Service Error"})
        logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
        return await responseMaker(statusCode=200, requestId=requestId, data={"msg":"User address edited succeessfully"})
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return await responseMaker(statusCode=400, requestId=requestId, errors=[await errorMaker("addressDoesNotExist")])



async def getAllAddressWithInPerimeterFromDb(requestId, dbConn, payload):
    """
    Function to find all the cordinate wuth in given response

    Args:
        requestid, db connection, payload

    Returns:
        list of all cordinate with perimeter
    """
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    resp = []
    perimeter = payload["distance"]
    ipLatitude = payload["latitude"]
    inLongitude = payload["longitude"]
    dbResp = jsonable_encoder(dbConn.query(Address.latitude, Address.longitude).all())

    for address in dbResp:
        distance = await distanceFinder(requestId=requestId, lat1=address["latitude"], lat2=ipLatitude, long1=address["longitude"], long2=inLongitude)
        if distance <= perimeter:
            resp.append(address)
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return await responseMaker(statusCode=200, requestId=requestId, data=resp)


async def distanceFinder(requestId, lat1, lat2, long1, long2):
    """
    Function to calculate the distance between two points

    Args:
        latitude and longitude of twoq points

    Returns:
        distance(K.m.) between these two points
    """
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " started"))
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (long2 - long1) * math.pi / 180.0
 
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    logger.info('{} {}'.format(requestId, sys._getframe().f_code.co_name + " ended"))
    return rad * c