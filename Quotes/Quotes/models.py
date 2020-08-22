'''
1. Create the database schema
'''

import sqlalchemy
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()

def db_connect():
    # Performs database connection using database settings from settings.py
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)

# Association Table for many-to-many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
quote_tag = Table('quote_tag', Base.metadata,
                  Column('quote_id', Integer, ForeignKey('quote.id')),
                  Column('tag_id', Integer, ForeignKey('tag_id'))
)

class Quote(Base):
    __tablename__ = "quote"
    
    id = Column(Integer, primary_key=True)
    quote_content = Column('quote_content', Text())
    author_id = Column(Integer, ForeignKey('author.id')) # many quotes to one author
    tags = relationship('Tag', secondary = 'quote_tag', lazy = 'dynamic', backref = 'quote') # many-to-many for quote and tag

class Author(Base):
    __tablename__ = "author"
    
    id = Column(Integer, primary_key = True)
    name = Column('name', String(50), unique = True)
    birthday = Column('bio', Text())
    bornlocation = Column('bornlocation', String(50))
    bio = Column('bio', Text())
    quotes = relationship('Quote', backref = 'author') # one author to many quotes
    
class Tag(Base):
    __tablename__ = "tag"
    
    id = Column(Integer, primary_key = True)
    name = Column('name', String(30), unique = True)
    quotes = relationship('Quote', secondary = 'quote_tag', lazy = 'dynamic', backref = 'tag') # many-to-many for quote and tag
