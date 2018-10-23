# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from medical_crawler.items import ResourceLink
import json


class DoctorsSpider(scrapy.Spider):
    name = 'doctors'

    def start_requests(self):
        for url in self.city_doctors_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in LinkExtractor(restrict_css="div.town_vrach_speclist").extract_links(response):
            yield scrapy.Request(url=link.url, callback=self.parse_doctor_links)

    def parse_doctor_links(self, response):
        for doctor_link in LinkExtractor(restrict_css=".fio").extract_links(response):
            yield ResourceLink(name=doctor_link.text, url=doctor_link.url)

        pagers = response.css('span.page a::attr("href")').extract()

        if not len(pagers) == 0 or len(pagers) == 1 and (
                pagers[0] != "?page=2" or response.url.split("/")[-1] == "?page=3"):
            yield response.follow(pagers[-1], self.parse_doctor_links)

    def city_doctors_urls(self):
        with open('cities.json') as cities:
            return [city["url"] + "vrach/" for city in json.load(cities)]
