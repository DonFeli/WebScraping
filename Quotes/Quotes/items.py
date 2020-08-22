'''
if you designed a relational database before, you may ask: should I have two items QuoteItem and AuthorItem to better represent the data logically? The answer is yes you could but not recommended in this case because items are returned by Scrapy in an asynchronous way and you will have additional logic added to match the quote item with its corresponding item — it’s much easier to put the related quote and author in one item in this case
'''

import scrapy
from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
# MapCompose apply one or more processing functions to a Field
# TakeFirst return the first value of the list
from datetime import datetime


def remove_quotes(text):
    # strip : remove left and right characters
    text = text.strip(u'\u201c'u'\u201d')
    return text

def convert_date(text):
    return datetime.strptime(text, '%B %d, %Y')

def parse_location(text):
    return text[3:]


class QuoteItem(Item):
    quote_content = Field(
        input_processor = MapCompose(remove_quotes),
        output_processor = TakeFirst()
    )
    author_name = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    author_birthday = Field(
        input_processor = MapCompose(convert_date),
        output_processor = TakeFirst()
    )
    author_bornlocation = Field(
        input_processor = MapCompose(parse_location),
        output_processor = TakeFirst()
    )
    author_bio = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    tags = Field()

