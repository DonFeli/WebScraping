import scrapy
from MSR.items import MsrItem

class MsrPipeline:
    def file_path(self, request, response=None, info=None):                 
        file_name: str = request.url.split("/")[-1]
        return file_name

class MsrItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

class MairieStRestitut_Spider(scrapy.Spider):
    name = 'item'
    
    def start_requests(self):
        url = 'https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux/'
        yield scrapy.Request(url = url, callback = self.parse_item)

    def parse_item(self, response):
        pdf_urls = response.css('a[href$=".pdf"]::attr(href)').getall()
        
        for pdf_url in pdf_urls: 
            item = MsrItem()
            item['file_urls'] = [pdf_url]
            yield item
        
        #  'item_scraped_count': 47
        
        # for pdf_url in pdf_urls: 
        #     yield { 'pdf_url' : pdf_url}    
        # {'pdf_url': 'http://saintrestitut-mairie.fr/wp-content/uploads/sites/212/2018/02/CR-CM-du-23-janvier-2018.pdf'}
        # {'pdf_url': 'http://saintrestitut-mairie.fr/wp-content/uploads/sites/212/2018/01/1343_001.pdf'}
        # {'pdf_url': '/wp-content/uploads/sites/212/2017/12/CR_CM_du_05_12_20170855.pdf'}
        
        

