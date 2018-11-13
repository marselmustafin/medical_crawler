# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from drugs_crawler.items import ConsumerDrugReview
import json

class ConsumersDrugsReviewSpider(scrapy.Spider):
    name = 'consumers_drugs_reviews'

    custom_settings = {
        'ITEM_PIPELINES': {
            'drugs_crawler.pipelines.UrlDuplicatesPipeline': 300
        },
    }

    def start_requests(self):
        for url in self.drugs_urls():
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta["reviews_class"] = "table.drug_comments tr.rate"
            yield request

    def parse(self, response):
        url = response.url
        for comment_div in response.css(response.meta["reviews_class"]):
            yield self.parse_review(comment_div, url)

    def parse_review(self, review_div, url):
        rate = review_div.css('div.rate_stars__tooltipster tr td::text')

        if not rate:
            return ConsumerDrugReview(
                url = url,
                comment = review_div.css("p[class='comment2']::text").extract_first(),
                date = review_div.css("div[class='datetime']::text").extract_first(),
            )

    def drugs_urls(self):
        with open('drugs.json') as drugs:
            return ['https://protabletky.ru' + drug["url"] for drug in json.load(drugs)]
