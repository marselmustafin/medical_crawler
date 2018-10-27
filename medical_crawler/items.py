# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ResourceLink(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class Doctor(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    specialities = scrapy.Field()
    institution_id = scrapy.Field()
    institution_name = scrapy.Field()
    institution_city = scrapy.Field()


class InstitutionComment(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    institution_id = scrapy.Field()
    institution_name = scrapy.Field()
    institution_city = scrapy.Field()
    author_name = scrapy.Field()
    author_operator = scrapy.Field()
    avg_text = scrapy.Field()
    avg_rate = scrapy.Field()
    datetime = scrapy.Field()
    pos_content = scrapy.Field()
    neg_content = scrapy.Field()
    content = scrapy.Field()
    reply_datetime = scrapy.Field()
    reply = scrapy.Field()
    doctor_name = scrapy.Field()
