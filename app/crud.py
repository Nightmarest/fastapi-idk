from sqlalchemy.orm import Session
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


def create_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    db_review = models.Review(
        stars=review.stars,
        comment=review.comment,
        user_id=user_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()
