from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker



DATABASE_URL = "postgresql://postgres:pass@localhost:5432/digi_db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('category.id'))
    
    parent = relationship('Category', remote_side=[id], backref='subcategories')


class Product(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    
    category = relationship('Category', backref='products')

class ProductAttribute(Base):
    __tablename__ = 'product_attributes'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    attribute_name = Column(Text, nullable=False)
    attribute_value = Column(Text)
    
    product = relationship('Product', backref='attributes')
 
class ProductVariant(Base):
    __tablename__ = 'product_variants'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    variant_name = Column(Text, nullable=False)
    price = Column(Integer)
    stock_quantity = Column(Integer, nullable=False)
    
    product = relationship('Product', backref='variants')

Base.metadata.create_all(engine)
