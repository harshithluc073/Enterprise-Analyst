from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FinancialRecord(Base):
    __tablename__ = "financial_records"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    department = Column(String, nullable=False)
    category = Column(String, nullable=False)
    vendor = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)

    def __repr__(self):
        return f"<FinancialRecord(vendor='{self.vendor}', amount={self.amount})>"