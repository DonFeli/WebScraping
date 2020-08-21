import scrapy


class WikiSpider(scrapy.Spider):
    
    name = 'wiki'
    
    urls = ['http://https://en.wikipedia.org/wiki/Category:Information_visualization_experts/']

    for url in urls:
        yield scrapy.Request( url = url, callback = self.parse)

    def parse(self, response):
        