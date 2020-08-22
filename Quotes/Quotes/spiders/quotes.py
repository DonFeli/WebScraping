import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        
        self.logger.info("Bonjour")
        
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),                'tag': quote.css('.tag::text').getall(),
            }
        
            # Scrape the author's bio
            # pourquoi un + ?
            author_url = quote.css('.author + a::attr(href)').get()
            # Goes to the author page
            yield response.follow(author_url, callback = self.parse_author)
        
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
        # Asynchronous : may not be processed in sync with the corresponding quote
        yield {
            'author_name' : response.css('.author-title::text').get(),
            'author_birthday' : response.css('.author-born_date::text').get(),
            'author_bornlocation' : response.css('.author-born-location::text').get(),
            'author_bio' : response.css('.author-description::text').get(),
        }