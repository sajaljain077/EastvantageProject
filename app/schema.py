from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import VARCHAR, INT
from app.database import Base


class Users(Base):
    __tablename__ = "Users"

    id = Column(INT, primary_key=True, nullable = False, autoincrement = True)
    email = Column(VARCHAR(256), unique=True, index=True)
    hashedPassword = Column(VARCHAR(256))
    ADDRESS = relationship("Users", backref="Address")


class Address(Base):
    __tablename__ = "Address"

    id     = Column(INT, primary_key=True)
    userId = Column(ForeignKey("Users.id"))
    latitude = Column(Float)
    longitude = Column(Float)

