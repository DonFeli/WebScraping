import scrapy


class MairieStRestitut_Spider(scrapy.Spider):
    name = 'msr'

    def start_requests(self):
        url = 'https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux/'
        yield scrapy.Request(url = url, callback = self.parse_pdf)
        yield scrapy.Request(url = url, callback = self.parse_name)

    # Probleme avec certains filename : 1106_001.pdf
    #                                   CR-CM-du-10-d%C3%A9cembre-2019.pdf
    # Solution : parser le texte puis joindre le nom au pdf (dict?)

    def parse_pdf(self, response):

        for pdf_url in response.css('a[href$=".pdf"]::attr(href)'):
            yield response.follow(pdf_url, callback = self.save_pdf)
 
            
    def parse_name(self, response):

        for pdf_url in response.css('a::text'):
            yield response.follow(pdf_url, callback = self.save_pdf)


    def save_pdf(self, response):
        

        filename = response
        
        self.logger.info('Saving PDF %s', filename)
        with open(path, 'wb') as f:
            f.write(response.body)
            

