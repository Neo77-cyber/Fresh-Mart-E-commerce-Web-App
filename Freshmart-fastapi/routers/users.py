from fastapi.security import OAuth2PasswordRequestForm
from fastapi import  Depends, HTTPException, APIRouter
from datetime import timedelta
import jwt
from typing import Dict
from utils.token import get_user,create_access_token, password_context,oauth2_scheme, authenticate_token
from database.models import User
from database.secrets import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES



router = APIRouter(prefix='',
                   tags=['users'])




@router.post('/register')
async def register(username: str, password: str):
    existing_user = await get_user(username)
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already exists')
    hashed_password = password_context.hash(password)
    user = await User.create(username=username, password_hash=hashed_password)
    return {"message": "Registered successfully"}


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(user: User = Depends(authenticate_token)):
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return {"message": "Protected route accessed successfully."}
    

@router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}