# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from medical_crawler.items import City


class CitiesSpider(scrapy.Spider):
    name = 'cities'
    start_urls = ["https://prodoctorov.ru/regions/"]

    def parse(self, response):
        for region_link in LinkExtractor(restrict_css="div.regions").extract_links(response):
            yield scrapy.Request(url=region_link.url, callback=self.parse_cities)

    def parse_cities(self, region_response):
        for city_path in LinkExtractor(restrict_css="table.rgns").extract_links(region_response):
            yield City(name=city_path.text, url=city_path.url)
