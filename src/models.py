from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, Date, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.db import Base
from src.schemas import CategoryEnum


class WikiPage(Base):
    __tablename__ = 'wiki_pages'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[Optional[str]] = mapped_column(String)
    author_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    publication_date: Mapped[datetime] = mapped_column(Date, nullable=False)


class MagazineModel(Base):
    __tablename__ = 'magazines'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR, index=True, unique=True, nullable=False)
    author: Mapped[str] = mapped_column(VARCHAR, index=True, nullable=False)
    publication_date: Mapped[datetime] = mapped_column(Date, index=True, nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(Enum(CategoryEnum), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    contents: Mapped[list['MagazineContentModel']] = relationship('MagazineContentModel', back_populates="magazine")


class MagazineContentModel(Base):
    __tablename__ = 'magazine_contents'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR, index=True, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    vector_representation: Mapped[str] = mapped_column(String, nullable=False)
    magazine_id: Mapped[int] = mapped_column(Integer, ForeignKey('magazines.id'), nullable=False)
    magazine: Mapped[MagazineModel] = relationship("MagazineModel", back_populates="contents")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
