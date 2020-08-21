import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.pipelines.files import FilesPipeline

class ZipfilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
     file_name: str = request.url.split("/")[-1]
     return file_name

class ZipfilesItem(scrapy.Item):
     file_urls = scrapy.Field()
     files = scrapy.Field

class NirsoftSpider(CrawlSpider):
    name = 'nirsoft'
    allowed_domains = ['www.nirsoft.net']
    start_urls = ['http://www.nirsoft.net/']

    rules = (
        Rule(LinkExtractor(allow=r'utils/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        file_url = response.css('.downloadline::attr(href)').get()
        file_url = response.urljoin(file_url)
        file_extension = file_url.split('.')[-1]
        if file_extension not in ('zip', 'exe', 'msi'):
            return
        item = ZipfilesItem()
        item['file_urls'] = [file_url]
        item['original_file_name'] = file_url.split('/')[-1]
        yield item

        # item = {}
        # #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # #item['name'] = response.xpath('//div[@id="name"]').get()
        # #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
