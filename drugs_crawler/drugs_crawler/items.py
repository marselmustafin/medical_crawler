# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Drug(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    drug_type = scrapy.Field()
    rating = scrapy.Field()
    reviews_count = scrapy.Field()
    description = scrapy.Field()

class DoctorDrugReview(scrapy.Item):
    url = scrapy.Field()
    comment = scrapy.Field()
    comment_plus = scrapy.Field()
    comment_minus = scrapy.Field()
    date = scrapy.Field()
    rate = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()

class ConsumerDrugReview(scrapy.Item):
    url = scrapy.Field()
    comment = scrapy.Field()
    date = scrapy.Field()

class DrugsGroups(scrapy.Item):
    url = scrapy.Field()


