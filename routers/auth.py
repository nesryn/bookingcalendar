from security import create_access_token, hash_password, verify_password
from fastapi import APIRouter, Depends, HTTPException
from schemas import Token, UserCreate,SignInRequest
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session 
from database import get_db
from models import User,UserRole,Project

router = APIRouter()

@router.post("/signup")
def create_user(data:UserCreate, db: Session = Depends(get_db)):
    exist = db.scalar(select(User).where(data.email == User.email ))
    if exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    project= Project(name=data.project.name, category_id=data.project.category_id)

    user = User(
        name=data.name,
        last_name=data.last_name,
        phone=data.phone,
        email=data.email,
        projects=[project],
        hashed_password=hash_password(data.password),
        role=UserRole.ADMIN
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/signin", response_model=Token)
def admin_signin(form: SignInRequest = Depends(),
    db: Session = Depends(get_db),):
        user = db.scalar(select(User).where(form.email == User.email))
        if user is None or not verify_password(form.password, user.hashed_password):
             raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        return Token(access_token=create_access_token(user.id))
