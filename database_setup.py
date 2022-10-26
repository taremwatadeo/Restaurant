import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'  # Table Information

    # Database Mappers
    name = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    course = Column(String(50))
    price = Column(String(6))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

 # insert at the end of file
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)  # Adds classes to the database as new tables
