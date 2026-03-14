from .base import Base

class User(Base):
    __tablename__ = 'users'                         #TODO: Implement the user class according to the scheme

class Order(Base):
    __tablename__ = 'orders'                        #TODO: Implement the service class according to the scheme

class AdditionalWork(Base):
    __tablename__ = 'additional_work_requests'      #TODO: Implement the additionalWork class according to the scheme

