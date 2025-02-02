from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter, Query
from app.models import models
from .database.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.schemas.dbschemas import Category, ReviewHistory
from app.tasks import log_activity
from typing import List
import datetime
app = FastAPI()

@app.get("/reviews/trends/", status_code=status.HTTP_200_OK, response_model=List[models.ShowTrend])
def get_top_categories(db: Session = Depends(get_db)):
    top_categories = db.query(
        Category.id,
        Category.name,
        Category.description,
        func.avg(ReviewHistory.stars).label('average_stars'),
        func.count(ReviewHistory.id).label('total_reviews')
    ).join(ReviewHistory, ReviewHistory.category_id == Category.id) \
    .group_by(Category.id) \
    .order_by(func.avg(ReviewHistory.stars).desc()) \
    .limit(5).all()
    tmp = str(datetime.datetime.now())
    log_activity.delay("/reviews/trends/", tmp)

    return top_categories


@app.get("/reviews/", status_code=status.HTTP_200_OK, response_model=List[models.ShowCategory])
def get_trend_for_catid(cat_id, db: Session = Depends(get_db),
                        skip: int = Query(0, alias="offset", ge=0),
                        limit: int = Query(15, alias="limit", ge=1, le=100)):
    if int(cat_id) < 1 or int(cat_id) > 15:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {cat_id} is not available !")
    result = db.query(
        ReviewHistory.id,
        ReviewHistory.text,
        ReviewHistory.stars,
        ReviewHistory.review_id,
        ReviewHistory.created_at,
        ReviewHistory.tone,
        ReviewHistory.sentiment,
        ReviewHistory.category_id
    ).filter(ReviewHistory.category_id == cat_id)\
    .order_by(ReviewHistory.created_at.desc())\
    .offset(skip)\
    .limit(limit)\
    .all()
    
    tmp = str(datetime.datetime.now())
    log_activity.delay(f"/reviews/{cat_id}", tmp)
    return result




#To create and insert date in database.
# import random
# import string
# import time
# @app.post("/", status_code=status.HTTP_201_CREATED)
# def createCategory(category: models.Category, db: Session = Depends(get_db)):
#     for i in range(1, 16):
#         categories = {1:"EchoBud",2:"SwiftCharge",3:"GlideMouse",4:"PixelPad",5:"AeroFan",6:"FlexiStand",7:"LumeLight",8:"BreezePur",9:"ChillMug",10:"TuneCast",11:"VisionCam",12:"TrackFit",13:"GripCase",14:"SteamPress",15:"ZenMat"}
#         descript = {1:"Wireless earbuds with noise cancellation.", 2:"Fast-charging power bank for on-the-go use.", 3:"Ergonomic wireless mouse with smooth tracking.", 4:"Compact tablet with a high-resolution display.", 5:"Portable mini fan with adjustable speed.", 6:"Foldable laptop stand with adjustable angles.", 7:"Smart LED lamp with voice control.", 8:"Air purifier with HEPA filter technology.", 9:"Temperature-controlled smart mug.", 10:"Bluetooth speaker with deep bass.", 11:"HD webcam with auto-focus and noise reduction.", 12:"Fitness tracker with heart rate monitor.", 13:"Shockproof phone case with anti-slip grip.", 14:"Handheld garment steamer for wrinkle-free clothes.", 15:"Memory foam yoga mat for extra comfort."}
#         categ = categories[i]
#         desc = descript[i]
#         new_cat = dbschemas.Category(name= categ, description=desc)
#         db.add(new_cat)
#         db.commit()
#         db.refresh(new_cat)
#         print(new_cat)

# @app.post("/category", status_code=status.HTTP_201_CREATED)
# def createReviewHistory(review: models.Review, db: Session = Depends(get_db)):
#     revids = ["zDRSo1ze0HyPAnCizttk", "yQdFIqHew5QcBb0t4tdd", "yDccBmIUFz8CmRbSb7Vc", "xX3mrRf8WZyyQzbdSLO4", "wlC04R2u9lMIOVvvuYQT", "wKjAO7JwsYJSQ51E4YlY", "rPjS8msRqfW3lhYXr7dx", "qf1wJACv8IHThLi7s1MN", "q3tmv88hKE5WlO0AACEQ", "n7z3V0WoWFEdAbwIhc7g", "mnjbhipZvt9EC3gqxqeE", "mAmD2efy4tRQGeOahxWM", "m6ZPMzAbaNOdJzWQC772", "lgZeEH7vtxRnsG5ZQ4M7", "kXmWhmJ1tiaI37KPGphy", "jjRFELykI2klMeT9JWZs", "jaBXqglqHyTBPzmwJz9i", "cqyUPgK1kxhgxv8uE6SJ", "c6GQwKNYp5Xz07Gp4BpW", "afPLwdtXIBLCBfyym21X", "aVG6V2DnFydkAnG4LcQm", "aTftWCMnGpdsJMWTXLbM", "Wha5vrC6FJrv36ZIG0S6", "W0HOWRIKLyRq8c76bhY3", "V4OonvjEGN7eabjIcgvK", "TwqtS0oE33rIa8nJd3gy", "RmvcHzv6b3lYRTDXVlpi", "QtAvlzxCrwEmaCqFZ0NB", "PweZh70BSKLwW8QHQxEB", "Pv820OIsSOnDgznIzvjN", "OEwgVnwV2Zan8s6aEHuS", "NI9goCyli04yMdrlAFAH", "LWCyxuvbnuzb37uaZS1R", "KevxXZwSRRN2j6qOKTTG", "KY6Jsr9apBi4JB8SDCYd", "K3EJEM9A82g7vhczVLpP", "HVp8oYgd9Nv61y3nI1k7", "H2yjoog7XbJ1OGNYbu0Q", "GRyplUscU6KUoafSU3az", "G6PILlMtsSm3IVnljJeh", "DWSNGIRVgzOk9NTqoAWV", "CICHWYvJJX4rwim9zHaU", "C4Z5Bzqen0ZSPolMPrTd", "BRgw9D17lsaMNyAcO2BR", "9nW5CI5aicGJCk3yRF05", "9K0sKInovQcPQnOQ586R", "9Dpo8ZfzTxDkBPrO46L8", "5T1Z7sC1sGyPUc4Yrs7j", "3w2IYct7M6MR7t7ku12S", "293C6MwBnvYHSj4S9COy"]
#     for i in range(50):
#         sentiments = {1:"Positive", 2:"Neutral", 3:"Negative"}
#         tone = {1:"Happy", 2:"Sad", 3:"Angry", 4:"Sarcastic", 5:"Formal", 6:"Casual", 7:"Excited", 8:"Disappointed"}
#         tx = ''.join(random.choices(string.ascii_letters, k=random.randint(80, 100)))
#         sts = random.randint(1,10)
#         #revid = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
#         revid = revids[random.randint(0,49)]
#         tn = tone[random.randint(1,8)]
#         snt = sentiments[2]
#         if sts < 4:
#             snt = sentiments[3]
#         if sts > 7:
#             snt = sentiments[1]
#         catid = random.randint(1, 15)
#         new_review = dbschemas.ReviewHistory(text=tx, stars=sts, review_id = revid, tone= tn, sentiment=snt, category_id = catid)
#         db.add(new_review)
#         db.commit()
#         db.refresh(new_review)
#         time.sleep(3)
#         print(new_review)