from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.config import Base


class SpreadAlert(Base):
    __tablename__ = "spread_alerts"

    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String(50), unique=True, index=True)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f'''<SpreadAlert(
            id={self.id}, 
            market_id={self.market_id}, 
            percentage={self.percentage}, 
            created_at={self.created_at}, 
            updated_at={self.updated_at}\n)>'''
