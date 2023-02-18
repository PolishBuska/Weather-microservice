
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,text, ForeignKey
metadata = Base.metadata

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True,nullable=False)
    city = Column(String)
    weather = Column(String,nullable=False)
    temperature = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))

