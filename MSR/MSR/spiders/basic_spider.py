import scrapy

class MairieStRestitut_Spider(scrapy.Spider):
    name = 'basic'
    
    def start_requests(self):
        url = 'https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux/'
        yield scrapy.Request(url = url, callback = self.parse_pdf)

    def parse_pdf(self, response):
        for pdf_url in response.css('a[href$=".pdf"]::attr(href)'):
            yield response.follow(pdf_url, callback = self.save_pdf)

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)


# Probleme avec certains filename : 
# 1106_001.pdf
# CR-CM-du-10-d%C3%A9cembre-2019.pdf

# A tester : parser le texte puis joindre au pdf file

# 1 : dans le meme parse puis follow save_pdf

        # for pdf_url in response.css('a[href$=".pdf"]::attr(href)'):
        #     yield response.follow(pdf_url, callback = self.save_pdf)
            
        # for pdf_name in response.css('a::text').get():
        #     yield response.follow(pdf_name, callback = self.save_pdf)
        
     
# 2 : tout dans le meme parse
                
#     def parse_pdf(self, response):
#         for pdf in response.css('div.entry-content'):
#             {
#                 "name" : pdf.css('a::text').get(),
#                 "file" : pdf.css('a[href$=".pdf"]::attr(href)').get(),  
#             }
#             with open(name, 'wb') as f:
#                 f.write(response.body)


# 3 : dans 3 parse follow a la suite 

    
#     def start_requests(self):
#         url = 'https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux/'
#         yield scrapy.Request(url = url, callback = self.parse_pdf)

#     def parse_pdf(self, response):
#         for pdf_url in response.css('a[href$=".pdf"]::attr(href)'):
#             yield response.follow(pdf_url, callback = self.save_pdf)

#      def save_pdf(self, response):
#          self.logger.info('Saving PDF %s', pdf_name)
#          with open(pdf_name, 'wb') as f:
#              f.write(response.body)

# 4 : dans 2 parse following to save_pdf


