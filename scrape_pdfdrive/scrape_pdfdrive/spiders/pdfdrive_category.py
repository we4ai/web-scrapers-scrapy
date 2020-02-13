import scrapy
from scrapy.http import Request
import time
'''
This can be tested by executing:
scrapy crawl pdfdrive-category -a query=3 -o data.json
'''
class CategorySpider(scrapy.Spider):
    name='pdfdrive-category'
    allowed_domains = ['pdfdrive.com']

    def __init__(self, query):
        self.start_urls = ['https://www.pdfdrive.com/category/'+str(query)]

    def parse(self, response):
        links = [response.urljoin(link) for link in \
        response.xpath('//*[@class="file-right"]/a/@href').extract()]

        """
        Write code to fetch all the books details of a specific category
        """
        for link in links:
            yield Request(link, callback = self.parse_page)

        next_page_url = response.urljoin(response.xpath("//a[@rel='next']/@href").extract_first())
        yield Request(next_page_url)

    def parse_page(self, response):
        book_title = response.xpath('//h1[@class="ebook-title"]/text()').extract_first()
        pages, year, size, _ = response.\
        xpath("//div[@class='ebook-file-info']/span[@class='info-green']/text()").extract()
        tags = response.xpath('//div[@class="ebook-tags"]/a/text()').extract()
        author =  response.xpath('//span[@itemprop="creator"]/text()').extract_first()

        tags = ','.join(tags)
        download_link = response.urljoin(response.xpath("//a[@id='download-button-link']/@href").extract_first())
        yield {
        'Title' : book_title,
        'Page' : pages,
        'Year' : year,
        'Size' : size,
        'Author' : author,
        'Tags' : tags,
        'Download Link' : download_link,
        }
