# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class WikiItem(Item):
    name = Field()
    bio = Field()
    works = Field()
    
