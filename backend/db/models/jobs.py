from backend.db.database import Base 
from sqlalchemy import Column,Integer,Date,String,Boolean,TIMESTAMP,ForeignKey,ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

class Jobs(Base):
    
    __tablename__="jobs"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    company = Column(String,nullable=False)
    company_url = Column(String)
    location = Column(String,nullable=False)
    description = Column(String,nullable=False)
    date_posted = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))
    is_active = Column(Boolean(),default=True)
    owner_id = Column(Integer,ForeignKey("user.id"))
    owner = relationship("User",back_populates='jobs')