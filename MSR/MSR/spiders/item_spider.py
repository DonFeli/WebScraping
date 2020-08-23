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
        
        
        # for pdf_url in response.css('a[href$=".pdf"]::attr(href)'):
        #     yield response.follow(pdf_url, callback = self.save_pdf)
            
        # for pdf_name in response.css('a::text').get():
        #     yield pdf_name



# class MairieStRestitut_Spider(scrapy.Spider):
#     name = 'msr'

#     url = 'https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux/'

#     # Probleme avec certains filename : 1106_001.pdf
#     #                                  CR-CM-du-10-d%C3%A9cembre-2019.pdf
#     # Solution : parser le texte puis joindre le nom au pdf (dict?)
                
#     def parse_pdf(self, response):

#         for pdf in response.css('div.entry-content'):
#             {
#                 "name" : pdf.css('a::text').get(),
#                 "file" : pdf.css('a[href$=".pdf"]::attr(href)').get(),  
#             }
            
#             self.logger.info('Saving PDF %s', name)
            
#             with open(name, 'wb') as f:
#                 f.write(response.body)


# class MairieStRestitut_Spider(scrapy.Spider):
#     name = 'msr'
    
#     def start_requests(self):
#         url = 'https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux/'
#         yield scrapy.Request(url = url, callback = self.parse_pdf)

#     def parse_pdf(self, response):
#         for pdf_url in response.css('a[href$=".pdf"]::attr(href)'):
#             yield response.follow(pdf_url, callback = self.save_pdf)

#     def save_pdf(self, response):
#         path = response.url.split('/')[-1]
#         self.logger.info('Saving PDF %s', path)
#         with open(path, 'wb') as f:
#             f.write(response.body)

    # def save_pdf(self, response):
    #     self.logger.info('Saving PDF %s', pdf_name)
    #     with open(pdf_name, 'wb') as f:
    #         f.write(response.body)
