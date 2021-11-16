import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super(LeroySpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{query}/']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[contains(@class, "phytpj4_plp")]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.xpath('//a[@data-qa-pagination-item ="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_value('url', response.url)

        yield loader.load_item()