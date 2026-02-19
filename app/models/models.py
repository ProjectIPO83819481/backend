from sqlalchemy import BigInteger, func, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import BYTEA, TEXT, JSON
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'                         #TODO: Implement the user class according to the scheme

class Service(Base):
    __tablename__ = 'services'                      #TODO: Implement the service class according to the scheme

class Order(Base):
    __tablename__ = 'orders'                        #TODO: Implement the service class according to the scheme

class AdditionalWork(Base):
    __tablename__ = 'additional_work_requests'      #TODO: Implement the additionalWork class according to the scheme

class Photo(Base):
    __tablename__ = 'photos'                        #TODO: Implement the photo class according to the scheme