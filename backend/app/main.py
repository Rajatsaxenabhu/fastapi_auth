from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
from routes.api_auth import router
from routes.api_user import router1
from fastapi.security import OAuth2PasswordBearer
from security.secure import verify_token,ACCESS_TOKEN,update_access_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000"
]
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def verify_token_middlware(request: Request,call_next):
    if request.url.path in ["/auth/login","/auth/signup"]:
        return await call_next(request)
    access_token = request.cookies.get("access_token")

    if not access_token:
        return JSONResponse({"msg": "Access token not found"},status_code=403)
    try:
        access_payload = verify_token(access_token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Access token is invalid or expired")
    response = await call_next(request)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN * 60)
    return response


app.include_router(router)
app.include_router(router1)