import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
import urllib.parse
from scrapy.loader import ItemLoader


class WikiSpider(scrapy.Spider):
    
    name = 'wiki'

    def start_requests(self):
        url = 'http://en.wikipedia.org/wiki/Category:Information_visualization_experts'
        yield Request(url = url, callback = self.parse)

    # Recuperer les noms et les url de chaque InfoViz expert a partir de la page de catégorie où ils sont listés par ordre alphabétique
    def parse(self, response):        
        cat = response.css('div.mw-category-group')
        for c in cat:     
            name_item = c.css('a::attr(title)').get(),
            wikiItem = WikiItem(name = name_item)
            yield wikiItem
    
    #     print(type(abc_list))
    #     print('\nLe 1er de la liste est:\n\n', abc_list[0], '\n')
        
    #     for abc in abc_list:
    #         yield response.follow(url = abc, callback = self.parse_names)
    #         # TypeError: Cannot mix str and non-str arguments

            
    # def parse_names(self, response): 
        
    #     names = response.css('a::attr(title)').getall()
    #     print(names)
            
process = CrawlerProcess()
process.crawl(WikiSpider)
process.start()