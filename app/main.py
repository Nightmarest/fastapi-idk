from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from typing import Optional
from app import crud, models, schemas
from app.database import engine, get_db, Base
from app.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.deps import get_current_user

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Backend", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend"}


@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    created_user = crud.create_user(db=db, user=user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": created_user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": created_user.id,
        "email": created_user.email,
        "name": created_user.name,
    }


@app.post("/login", response_model=schemas.Token)
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.patch("/users/me", response_model=schemas.UserResponse)
def update_users_me(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.update_user_name(db=db, user=current_user, name=user_update.name)


@app.post("/casinos", response_model=schemas.CasinoResponse, status_code=status.HTTP_201_CREATED)
def create_casino(
    casino: schemas.CasinoCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_casino(db=db, casino=casino)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Casino with this name already exists"
        )


@app.get("/casinos", response_model=list[schemas.CasinoResponse])
def read_casinos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    casinos = crud.get_casinos(db, skip=skip, limit=limit)
    return casinos


@app.post("/reviews", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review: schemas.ReviewCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if casino exists
    casino = crud.get_casino(db, casino_id=review.casino_id)
    if not casino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Casino not found"
        )
    
    try:
        return crud.create_review(db=db, review=review, user_id=current_user.id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submitted a review for this casino"
        )


@app.get("/reviews", response_model=list[schemas.ReviewResponse])
def read_reviews(casino_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews(db, casino_id=casino_id, skip=skip, limit=limit)
    return reviews
