# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from drugs_crawler.items import DoctorDrugReview
import json
from IPython import embed

class DoctorsDrugsReviewSpider(scrapy.Spider):
    name = 'doctors_drugs_reviews'

    custom_settings = {
        'ITEM_PIPELINES': {
            'drugs_crawler.pipelines.UrlDuplicatesPipeline': 300
        },
    }

    def start_requests(self):
        for url in self.drugs_urls():
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta["reviews_class"] = "table.drug_rates tr.rate"
            yield request

    def parse(self, response):
        url = response.url
        for comment_div in response.css(response.meta["reviews_class"]):
            yield self.parse_review(comment_div, url)

    def parse_review(self, review_div, url):
        rate = review_div.css('div.rate_stars__tooltipster tr td::text')

        if rate:
            rate = rate[0].extract().strip().split(' ')[1]
            return DoctorDrugReview(
                url = url,
                comment = review_div.css("p[class='comment']::text").extract_first(),
                comment_plus = review_div.css("p[class='comment_plus']::text").extract_first(),
                comment_minus = review_div.css("p[class='comment_minus']::text").extract_first(),
                date = review_div.css("div[itemprop='datePublished']::text").extract_first(),
                rate = rate,
                author = review_div.css("span[itemprop='name']::text").extract_first(),
                author_url = review_div.css("a[class='fio']::attr(href)").extract_first()
            )

    def drugs_urls(self):
        with open('drugs.json') as drugs:
            return ['https://protabletky.ru' + drug["url"] for drug in json.load(drugs)]
