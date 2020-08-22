import scrapy
from scrapy.loader import ItemLoader
from Quotes.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        quotes = response.css('div.quote')
        
        # Item Loader enables pre/post processing : raw data obtained from the css selector may need to be further parsed (quotation marks, birthday string, 'in' born location)
        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector = quote)
            loader.add_css('quote_content', '.text::text')
            loader.add_css('tags', '.tag::text')
            quote_item = loader.load_item()
            '''
            # Before Item Loader
            yield {
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),                'tags': quote.css('.tag::text').getall(),
            }
            '''
            # Scrape the author's bio
            author_url = quote.css('.author + a::attr(href)').get() # + ?
            # Goes to the author page + pass the metadata from one page to another
            yield response.follow(author_url, callback = self.parse_author, meta = {'quote_item' : quote_item})
        
        '''   
        # Scrape the next page : option 1
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # get the full url 
            next_page = response.urljoin(next_page)
            # sends new request to the next page and call the same parse function to get the quotes from the new page
            yield scrapy.Request(next_page, callback = self.parse)
        '''
        # Scrape the next page : option 2
        for a in response.css('li.next a'):
            # 'follow' support relative urls and automatically use the 'href' for 'a'
            yield response.follow(a, callback = self.parse)
            
    def parse_author(self, response):
        #  RuntimeError: To use XPath or CSS selectors, ItemLoadermust be instantiated with a selector
        # Solution : add quotes loop + selector
        # à investiger 
        # Pb : items scraped = 0
        quotes = response.css('div.quote')
        
        for quote in quotes:
            # quote_item = response.meta['quote_item']
            loader = ItemLoader(item = quote_item, selector = quote, reponse = response)
            loader.add_css('author_name', '.author-title::text')
            loader.add_css('author_birthday', '.author-born-date::text')
            loader.add_css('author_bornlocation', '.author-born-location::text')
            loader.add_css('author_bio', '.author-description::text')
            yield loader.load_item()
        '''
        Before ItemLoader
        # Asynchronous : may not be processed in sync with the corresponding quote
        # 'author_name' same as 'author'
        yield {
            'author_name' : response.css('.author-title::text').get(),
            'author_birthday' : response.css('.author-born-date::text').get(),
            'author_bornlocation' : response.css('.author-born-location::text').get(),
            'author_bio' : response.css('.author-description::text').get(),
        }
        '''