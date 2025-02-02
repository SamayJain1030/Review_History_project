from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: str

class Category(CategoryBase):
    class Config():
        orm_mode =  True
        

class ReviewBase(BaseModel):
    text: str
    stars: int
    review_id: str
    tone: str
    sentiment: str
    category_id: int
    
class Review(ReviewBase):
    class Config():
        orm_mode =  True
        
        
class ShowTrend(BaseModel):
    id: int
    name: str
    description: str
    average_stars: float
    total_reviews: int
    class Config():
        orm_mode = True
        
        
class ShowCategory(BaseModel):
    id: int
    text: str
    stars: int
    review_id: str
    created_at: datetime
    tone: str
    sentiment: str
    category_id: int