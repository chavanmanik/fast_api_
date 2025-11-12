from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import auth, models, database

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------- REGISTER --------------------
@router.post("/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = auth.get_password_hash(password)
    user = models.User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully", "username": user.username}


# -------------------- LOGIN --------------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    refresh_token = auth.create_refresh_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "username": user.username
    }


# -------------------- REFRESH TOKEN --------------------
@router.post("/refresh")
def refresh_token(refresh_token: str):
    username = auth.verify_refresh_token(refresh_token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    new_access_token = auth.create_access_token(data={"sub": username})
    return {"access_token": new_access_token, "token_type": "bearer"}
