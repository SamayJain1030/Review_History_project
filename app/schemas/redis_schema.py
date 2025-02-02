from sqlalchemy import Column, BigInteger, VARCHAR
from app.base import Base

class AccessLog(Base):
    __tablename__ = 'accesslog'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(VARCHAR)
    timestamp = Column(VARCHAR)