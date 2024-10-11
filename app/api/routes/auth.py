from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse, Token
from app.crud.user import create_user
from app.core.security import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from app.db.database import get_db
from app.schemas.user import UserResponse
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    created_user = await create_user(db, user.email, user.username, user.password)
    if not created_user:
        raise HTTPException(status_code=400, detail="Email or username already registered.")
    return UserResponse.model_validate(created_user)

@router.post("/login", response_model=Token)
async def login_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected-route")
async def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}! You have access to this protected route."}