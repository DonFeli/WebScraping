import scrapy
from scrapy import Request


class MsrSpider(scrapy.Spider):
    name = 'msr'
    allowed_domains = ['https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux/']
    start_urls = ['http://https://saintrestitut-mairie.fr/comptes-rendus-des-conseils-municipaux//']

    def parse(self, response):
        for href in response.css('a::attr(href)').get():
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_article
            )

    def parse_article(self, response):
        for href in response.css('a[href$=".pdf"]::attr(href)').get():
            yield Request(
                url=response.urljoin(href),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
