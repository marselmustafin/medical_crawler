# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from drugs_crawler.items import DrugsGroups
import json

class DrugsGroupsSpider(scrapy.Spider):
    name = 'drugs_groups'

    custom_settings = {
        'ITEM_PIPELINES': {
            'drugs_crawler.pipelines.UrlDuplicatesPipeline': 300
        },
    }

    def start_requests(self):
        yield scrapy.Request(url= 'https://protabletky.ru/groups/', callback=self.parse)

    def parse(self, response):
        for pharm_tags in response.xpath('//*[@id="content"]/div/div/div/a/@href'):
            yield DrugsGroups(url= 'https://protabletky.ru' + pharm_tags.extract())

