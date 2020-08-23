import scrapy


class MairieStRestitut_Spider(scrapy.Spider):
    name = 'msr'

    def start_requests(self):
        url = 'https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux/'
        yield scrapy.Request(url = url, callback = self.parse_pdf)

    def parse_pdf(self, response):
        pdf_urls = response.css('a[href$=".pdf"]::attr(href)').getall()
        
        for pdf_url in pdf_urls:
            yield response.follow(pdf_url, callback = self.save_pdf)

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
