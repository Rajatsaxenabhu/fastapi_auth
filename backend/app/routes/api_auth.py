from fastapi import FastAPI, HTTPException, Depends, Response ,Request ,APIRouter
from fastapi.responses import JSONResponse
from fastapi import Request
from db.session import get_db
from sqlalchemy.orm import Session
from schema.user import UserCreate,UserVerify
from logic.user import UserService
from security.secure import create_access_token,create_refresh_token,ACCESS_TOKEN,REFRESH_TOKEN,verify_token

router = APIRouter()


@router.post("/signup")
async def signup(Data:UserCreate,db:Session=Depends(get_db)):
    user_service = UserService(db)
    return UserService.create_user(user_service,user_data=Data)


@router.post("/login")
async def login(Data:UserVerify,response: Response,db:Session=Depends(get_db)):
    user_service = UserService(db)
    if UserService.verify_user(user_service,user_data=Data):
        data = {"values":Data.email}
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        response = JSONResponse({"msg": "Login successful"},status_code=200)
        response.set_cookie(
        key="access_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN * 60
        )
        response.set_cookie(
            key="refresh_token", value=refresh_token, httponly=True, max_age=REFRESH_TOKEN * 24 * 60 * 60
        )
        return response
    
@router.post("/refresh")
async def refresh(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=403, detail="Access token not found")    
    
    data = None
    response = JSONResponse({"msg": "Token refreshed successfully"},status_code=200)
    access_token = create_access_token(data)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN * 60)
    return response