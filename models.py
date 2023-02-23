from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP,text
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
    wind = Column(String)

