import re
import textract
from itertools import chain
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tempfile import NamedTemporaryFile

control_chars = ''.join(map(chr, chain(range(0, 9), range(11, 32), range(127, 160))))
CONTROL_CHAR_RE = re.compile('[%s]' % re.escape(control_chars))
TEXTRACT_EXTENSIONS = [".pdf", ".doc", ".docx", ""]

class CustomLinkExtractor(LinkExtractor):
    def __init__(self, *args, **kwargs):
        super(CustomLinkExtractor, self).__init__(*args, **kwargs)
        # Keep the default values in "deny_extensions" *except* for those types we want.
        self.deny_extensions = [ext for ext in self.deny_extensions if ext not in TEXTRACT_EXTENSIONS]

class M10(CrawlSpider):
    name = "m10"
    start_urls = [
        'https://www.mairie10.paris.fr/ma-mairie/conseil-d-arrondissement/comptes-rendus-du-conseil-d-arrondissement-208'
    ]
    def __init__(self, *args, **kwargs):
    # defines how content retrieved by Scrapy will be processed : we're just going to write any content scraped from one of our binary documents to a file, and ignore everything else
        self.rules = (Rule(CustomLinkExtractor(), follow=True, callback="parse_item"),)
        super(M10, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        if hasattr(response, "text"):
            # The response is text - we assume html. Normally we'd do something                                                                 
            # with this, but this demo is just about binary content, so.                                                                     
            pass
        else:
            # We assume the response is binary data                                            
            # One-liner for testing if "response.url" ends with any TEXTRACT_EXTENSIONS                                                                  
            extension = list(filter(lambda x: response.url.lower().endswith(x), TEXTRACT_EXTENSIONS))[0]
            if extension:
                # This is a pdf or something else that Textract can process               
                # Create a temporary file with the correct extension.    
                tempfile = NamedTemporaryFile(suffix=extension)
                tempfile.write(response.body)
                tempfile.flush()
                extracted_data = textract.process(tempfile.name)
                extracted_data = extracted_data.decode('utf-8')
                extracted_data = CONTROL_CHAR_RE.sub('', extracted_data)
                tempfile.close()
                
                with open("scraped_content.txt", "a") as f:
                    f.write(response.url.upper())
                    f.write("\n")
                    f.write(extracted_data)
                    f.write("\n\n")