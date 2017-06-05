from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Float,
    Boolean
)

from .meta import Base


class Car(Base):
    __tablename__ = 'cars'
    vin_num = Column(Integer, primary_key=True)
    make = Column(Unicode)
    year = Column(Integer)
    price = Column(Float(precision=2, asdecimal=True))
    model = Column(Unicode)
    mileage = Column(Integer)
    condition = Column(Unicode)
    doors = Column(Integer)
    color = Column(Unicode)
    in_stock = Column(Boolean)
    description = Column(Unicode)
