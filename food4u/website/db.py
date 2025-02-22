from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
import datetime


engine = create_engine("sqlite:///food4u.db", echo=False)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    address = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    phone = Column(Text, nullable=True)
    date_registered = Column(DateTime, nullable=False)
    industry = Column(Text, nullable=False)
    is_staff = Column(Boolean, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships to other tables
    reviews = relationship("Review", back_populates="writer")


class Supplier(Base):
    __tablename__ = 'Supplier'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(Text, nullable=False, unique=True)
    address = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    phone = Column(Text, nullable=True)
    date_registered = Column(DateTime, nullable=True)
    industry = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    products = relationship("Products", back_populates="supplier")
    reviews = relationship("Review", back_populates="supplier")


class Products(Base):
    __tablename__ = 'Products'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    supplier_id = Column(Integer, ForeignKey('Supplier.id'), nullable=False)
    name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=True)
    moq = Column(Integer, nullable=True)
    
    supplier = relationship("Supplier", back_populates="products")
    reviews = relationship("Review", back_populates="product")


class Review(Base):
    __tablename__ = 'Review'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    writer_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('Products.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('Supplier.id'), nullable=False)
    rating = Column(Integer, nullable=True)
    label = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    date = Column(DateTime, nullable=True)
    
    writer = relationship("User", back_populates="reviews")
    product = relationship("Products", back_populates="reviews")
    supplier = relationship("Supplier", back_populates="reviews")

Base.metadata.create_all(engine)

#print("hello")

session = SessionLocal()
try:
    test_supplier = Supplier(name="test supplsier", address="test address", email="tests email", phone="test phone", industry="test industry", description="test description")
    session.add(test_supplier)
    session.commit()
    query = select(User).where(User.id == 1)
    results = session.scalar(query)
    print("adsadasdassa")
    print(results)
    #data = [obj.to_dict() for obj in results]  # Assume your models have a to_dict method
except Exception as e:
    print(e)
    print("errorerrorerrorerror")
    session.rollback()
finally:
    session.close()