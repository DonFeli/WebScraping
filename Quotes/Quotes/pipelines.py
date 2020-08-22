'''
Saves the item to the database
'''
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from Quotes.models import Quote, Author, Tag, db_connect, create_table

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class QuotesPipeline:
    def process_item(self, item, spider):
        return item
    
class SaveQuotesPipeline(object):
    def __init__(self): 
        '''
        Initializes db conncetion and sessionmaker
        Creates tables
        '''
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind = engine)
    
    def process_item(self, item, spider):
        '''
        Save quotes in the database
        This method is called for every item pipeline component
        '''
        session = self.Session()
        quote = Quote()
        author = Author()
        tag = Tag()
        author.name = item["author_name"]
        author.birthday = item["author_birthday"]
        author.bornlocation = item["author_bornlocation"]
        author.bio = item["author_bio"]
        quote.quote_content = item["quote_content"]
        
        # Check whether the author exists
        exist_author = session.query(Author).filter_by(name = author.name).first()
        if exist_author is not None:
            quote.author = exist_author
        else :
            quote.author = author
            
        # Check whether the current quote has tags or not
        if "tags" in item:
            for tag_name in item["tags"]:
                tag = Tag(name = tag_name)
                # Check whether the current tag already exists in the database
                exist_tag = session.query(tag).filter_by(name = tag.name).first()
                if exist_tag is not None: 
                    tag = exist_tag
                quote.tags.append(tag)
        
        try:
            session.add(quote)
            session.commit()
        
        except:
            session.rollback()
            raise
        
        finally:
            session.close()
            
        return item

