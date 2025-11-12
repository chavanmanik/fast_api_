from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, database, auth
from app.services import user_service
from app.transformers import user_transformer

router = APIRouter(prefix="/users", tags=["Users"])

# --- Register new user ---
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing = db.query(auth.models.User).filter(auth.models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db, user)

# --- Login ---
@router.post("/login", response_model=schemas.TokenData)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# --- Get all registered users (JWT protected) ---
@router.get("/all")
def get_all_users(
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    users = user_service.get_all_users(db)
    return user_transformer.transform_users(users)

# --- Get current user info ---
@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user=Depends(auth.get_current_user)):
    return current_user
