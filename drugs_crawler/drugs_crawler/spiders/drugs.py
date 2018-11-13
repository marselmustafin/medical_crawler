# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from drugs_crawler.items import Drug
import json

class DrugsSpider(scrapy.Spider):
    name = 'drugs'

    custom_settings = {
        'ITEM_PIPELINES': {
            'drugs_crawler.pipelines.UrlDuplicatesPipeline': 300
        },
    }

    def start_requests(self):
        for url in self.drugs_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for drug_div in response.css("table.drug_list tr.drug_list__drug"):
            rating = drug_div.css('div.drug_stars_tooltipster tr td::text')
            reviews_count = drug_div.css('a.drug_list__rates_count::text').extract_first()
            if rating:
                rating = rating[0].extract().strip().split(' ')[1]
            if reviews_count:
                reviews_count = reviews_count.strip().split('\n')[0]

            yield Drug(url = drug_div.css('a.drug_list__drug_name::attr(href)').extract_first(),
                 name = drug_div.css('a.drug_list__drug_name::text').extract_first().strip(),
                 drug_type = response.css('h1::text').extract_first(),
                 rating = rating,
                 reviews_count = reviews_count,
                 description = drug_div.css('blockquote.drug_list__rate_quote::text').extract_first())

        next_page_url = response.css('span.page > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            print(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def drugs_urls(self):
        with open('drugs_groups.json') as drugs_groups:
            return [drug_group["url"] for drug_group in json.load(drugs_groups)]
