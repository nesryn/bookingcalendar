from __future__ import annotations
import enum
from sqlalchemy import String, ForeignKey, LargeBinary
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    STAFF_MEMBER = "staff_member"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100),  unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(30))
    role: Mapped[UserRole] = mapped_column(SAEnum(
            UserRole,
            values_callable=lambda e: [item.value for item in e],
        ),
        default=UserRole.USER,
        nullable=False,)
    projects: Mapped[list[Project]] = relationship(back_populates="owner")

class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    logo: Mapped[bytes | None] = mapped_column(
            LargeBinary,
            nullable=True,
        )
    
    owner_id:  Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="projects")
    
    category_id : Mapped[int] = mapped_column(ForeignKey("category.id"))
    category : Mapped[Category] = relationship()


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
