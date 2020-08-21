import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

class WikiSpider(scrapy.Spider):
    
    name = 'wiki'

    def start_requests(self):
        url = 'http://en.wikipedia.org/wiki/Category:Information_visualization_experts'
        yield scrapy.Request(url = url, callback = self.parse_links)

    def parse_links(self, response):        
        for link in response.css('div.mw-category-group'):
            name_item = link.css('a::text').get()
            url_item = link.css('a::attr(href)').get()
            wikiItem = WikiItem(name = name_item, url = url_item)
            yield wikiItem

            
process = CrawlerProcess()
process.crawl(WikiSpider)
process.start()