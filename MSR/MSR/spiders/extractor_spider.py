import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# CrawlSpider supports rules
class MSR_Extractor(CrawlSpider):

    name = "extractor"
    
    start_urls = ['https://saintrestitut-mairie.fr/']
    
    rules = (
        Rule(LinkExtractor(allow=r'/wp-content/uploads/sites/212/'), callback = 'parse_item', follow=True),
    )
    # ne marche pas car adresse uploads differente page Comptes Rendus
    
    def parse_item(self, response):
        file_url = response.css('a::attr(href)').get()
        # file_url = response.css('a::attr(href)').get()
        # file_url = response.urljoin(file_url)
        yield { 'file_url': file_url }