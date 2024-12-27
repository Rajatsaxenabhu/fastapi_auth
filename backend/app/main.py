from fastapi import FastAPI,Request,HTTPException
from routes.api_auth import router
from routes.api_user import router1
from fastapi.security import OAuth2PasswordBearer
from security.secure import verify_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app=FastAPI()

@app.middleware("http")
async def verify_token_middlware(request: Request, call_next):
    if request.url.path in ["/login","/signup"]:
        return await call_next(request)
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=403, detail="Access token not found")
    try:
        access_payload = verify_token(access_token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Access token is invalid or expired")
    response = await call_next(request)
    return response


app.include_router(router)
app.include_router(router1)

    


