# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from medical_crawler.items import Doctor
import json


class DoctorsSpider(scrapy.Spider):
    name = 'doctors'

    def start_requests(self):
        for url in self.institutions_doctors_lists_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        institution_id = response.url.split("/")[-3].split("-")[0]
        institution_name = response.css(
            "div.lpu-right").css("div[itemprop='name']::text").extract_first().strip()
        institution_city = response.css(
            "div.lpu-right").css("div[itemprop='name'] div::text").extract_first().strip()

        for doctor_division in response.css("div.appointment_container_doctorlist"):
            url = doctor_division.css("a.fio::attr(href)").extract_first()
            id = url.split("/")[-2].split("-")[0]
            name = doctor_division.css("span.surname::text").extract_first()

            specialities = [speciality.strip().lower() for speciality in doctor_division.css(
                "div.doctorlist_specialities::text").extract_first().split(",")]

            yield Doctor(
                url=url,
                id=id,
                name=name,
                specialities=specialities,
                institution_id=institution_id,
                institution_name=institution_name,
                institution_city=institution_city
            )

    def institutions_doctors_lists_urls(self):
        with open('institutions.json') as institutions:
            return [institution["url"] + "vrachi/#all" for institution in json.load(institutions)]
