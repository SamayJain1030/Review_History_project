from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, VARCHAR, CheckConstraint, func, DateTime, Sequence
from app.base import Base  # Import Base from base.py
from sqlalchemy.orm import relationship

class Category(Base):        
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(255), unique=True, nullable=False)
    description = Column(String)
    reviews = relationship("ReviewHistory", back_populates="category")

class ReviewHistory(Base):               #as this has a dependency on categoryid so created after categroy table
    __tablename__ = 'reviewhistory'
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    text = Column(VARCHAR, nullable=True)
    stars = Column(Integer, nullable=False)
    review_id = Column(VARCHAR(255))
    tone = Column(VARCHAR(255), nullable=True)
    sentiment = Column(VARCHAR(255), nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    category = relationship("Category", back_populates="reviews")
    __table_args__  = (
        CheckConstraint('stars > 0 AND stars < 11', name='stars_range'),
        )
    
    
