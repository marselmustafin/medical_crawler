# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ResourceLink(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

# class Comment(scrapy.Item):
#     comment_id = scrapy.Field()
#     author_operator = scrapy.Field()
#     author_hidden_phone_number = scrapy.Field()
#     rate = scrapy.Field()
#     title = scrapy.Field()
#     datetime = scrapy.Field()
#     pos_comment = scrapy.Field()
#     neg_comment = scrapy.Field()
#     content = scrapy.Field()
#     reply_datetime = scrapy.Field()
#     reply_content = scrapy.Field()
#     comment_doctor = scrapy.Field()
