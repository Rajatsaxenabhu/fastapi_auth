from fastapi import FastAPI, HTTPException, Depends, Response ,Request ,APIRouter
from fastapi.responses import JSONResponse
from fastapi import Request
from db.session import get_db
from sqlalchemy.orm import Session
from schema.user import People,del_data
from logic.user import DataService
from security.secure import create_access_token,create_refresh_token,ACCESS_TOKEN,REFRESH_TOKEN,verify_token

router1 = APIRouter()
async def verify_token_middleware(request: Request, call_next):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=403, detail="Access token not found")
    try:
        access_payload = verify_token(access_token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Access token is invalid or expired")
    return await call_next(request)

@router1.post('/people/add_val')
async def add_people(
    Data: People, 
    request: Request, 
    response: Response, 
    db: Session = Depends(get_db)):  
    user_data_service=DataService(db)
    try:
        new_id=user_data_service.add_value(Data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return JSONResponse({"msg": "Data added successfully","new_id":new_id},status_code=200)

@router1.post('/people/delete_val')
async def del_people(
    Data:del_data , 
    request: Request, 
    response: Response, 
    db: Session = Depends(get_db)): 
    user_data_service=DataService(db)
    print("okay")
    try:
        user_data_service.delete_value(Data.ID)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse({"msg": "Data deleted successfully"},status_code=200)   