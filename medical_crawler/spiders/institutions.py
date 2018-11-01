# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from medical_crawler.items import ResourceLink
import json


class InstitutionsSpider(scrapy.Spider):
    name = 'institutions'

    custom_settings = {
        'ITEM_PIPELINES': {
            'medical_crawler.pipelines.UrlDuplicatesPipeline': 300
        },
    }

    def start_requests(self):
        for url in self.city_institutions_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in LinkExtractor(restrict_css="ul.lpu_types").extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.parse_institutions_links)

    def parse_institutions_links(self, response):
        for institution_link in LinkExtractor(restrict_css="a.lpulist_name").extract_links(response):
            yield ResourceLink(name=institution_link.text.strip(), url=institution_link.url)

        pagers = response.css('span.page a::attr("href")').extract()

        if not len(pagers) == 0 or len(pagers) == 1 and (
                pagers[0] != "?page=2" or response.url.split("/")[-1] == "?page=3"):
            yield response.follow(pagers[-1], self.parse_institutions_links)

    def city_institutions_urls(self):
        with open('cities.json') as cities:
            return [city["url"] + "lpu/" for city in json.load(cities)]
