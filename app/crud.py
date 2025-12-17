from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas
from app.security import get_password_hash


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_name(db: Session, user: models.User, name: str):
    user.name = name
    db.commit()
    db.refresh(user)
    return user


def create_casino(db: Session, casino: schemas.CasinoCreate):
    db_casino = models.Casino(name=casino.name)
    db.add(db_casino)
    db.commit()
    db.refresh(db_casino)
    return db_casino


def get_casino(db: Session, casino_id: int):
    return db.query(models.Casino).filter(models.Casino.id == casino_id).first()


def get_casinos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Casino).offset(skip).limit(limit).all()


def create_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    db_review = models.Review(
        stars=review.stars,
        comment=review.comment,
        user_id=user_id,
        casino_id=review.casino_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews(db: Session, casino_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Review)
    if casino_id is not None:
        query = query.filter(models.Review.casino_id == casino_id)
    return query.offset(skip).limit(limit).all()
