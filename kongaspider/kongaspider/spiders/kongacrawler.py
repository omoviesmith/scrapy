import scrapy
from kongaspider.itemsloaders import KongaProductLoader
from kongaspider.items import KongaspiderItem
from urllib.parse import urlencode

API_KEY = '98ddd227-d656-4c50-bb4a-78764c038121'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class KongacrawlerSpider(scrapy.Spider):
    name = 'kongacrawler'
    #allowed_domains = ['https://www.jumia.com.ng']

    # These are the urls that we will start scraping
    def start_requests(self):
        start_urls = ['https://www.jumia.com.ng/tablets/?operating_system=Android&page=%d' % i for i in range(1,23)]

        for start_url in start_urls:
            yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse)

    def parse(self, response):
        tablets = response.css('article.prd._fb.col.c-prd')

        for tablet in tablets:

            konga = KongaProductLoader(item=KongaspiderItem(), selector=tablet)

            konga.add_css('name', 'h3.name::text')
            konga.add_css('price', 'div.prc::text')
            konga.add_css('url', 'a.core::attr(href)')
            
            yield konga.load_item()

            #next_page = response.css('[aria-label="Next Page"] ::attr("href")').get()

            #if next_page is not None:
            #    next_page_url = 'https://www.jumia.com.ng' + next_page
            #    yield response.follow(next_page_url, callback=self.parse)



        
