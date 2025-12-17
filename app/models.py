from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="user")


class Casino(Base):
    __tablename__ = "casinos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    reviews = relationship("Review", back_populates="casino")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    stars = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    casino_id = Column(Integer, ForeignKey("casinos.id"), nullable=False)

    user = relationship("User", back_populates="reviews")
    casino = relationship("Casino", back_populates="reviews")

    @property
    def author_name(self):
        return self.user.name if self.user else None

    __table_args__ = (
        CheckConstraint('stars >= 1 AND stars <= 5', name='check_stars_range'),
        UniqueConstraint('user_id', 'casino_id', name='unique_user_casino_review'),
    )
