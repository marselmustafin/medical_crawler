# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class ResourceLinksDuplicatesPipeline(object):

    def __init__(self):
        self.urls_seen = set()
        self.comment_ids_seen = set()
        self.doctor_ids_seen = set()

    def process_item(self, item, spider):
        if self.duplicated_link(item):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])
            return item

    def duplicated_link(self, item):
        return item.__class__.__name__ == "ResourceLink" and item['url'] in self.urls_seen


class DoctorsDuplicatesPipeline(object):

    def __init__(self):
        self.doctor_ids_seen = set()

    def process_item(self, item, spider):
        if self.duplicated_doctor(item):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.doctor_ids_seen.add(item['id'])
            return item

    def duplicated_doctor(self, item):
        return item.__class__.__name__ == "Doctor" and item['id'] in self.doctor_ids_seen


class CommentsDuplicatesPipeline(object):

    def __init__(self):
        self.comment_ids_seen = set()

    def process_item(self, item, spider):
        if self.duplicated_comment(item):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.comment_ids_seen.add(item['id'])
            return item

    def duplicated_comment(self, item):
        return item.__class__.__name__ == "InstitutionComment" and item['id'] in self.comment_ids_seen
