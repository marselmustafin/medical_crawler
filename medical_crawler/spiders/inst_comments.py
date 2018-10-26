# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from medical_crawler.items import InstitutionComment
from w3lib.html import remove_tags
import json
import re


class InstCommentsSpider(scrapy.Spider):
    name = 'inst_comments'
    base_url = "https://prodoctorov.ru"

    def start_requests(self):
        for institution_reviews_url in self.institutions_reviews_urls():
            request = scrapy.Request(
                url=institution_reviews_url, callback=self.parse)
            request.meta["comments_class"] = "table.rates tr"
            yield request

    def parse(self, response):
        if response.css("div.lpu-right"):
            self.set_institution_params(response.css("div.lpu-right"))

        url = response.url

        for comment_division in response.css(response.meta["comments_class"]):
            yield self.parse_comment(comment_division, url)

        doctor_comments_link = response.css(
            ".fetch_lpu_doctors_rates::attr(data-url)").extract_first()

        if doctor_comments_link:
            request = response.follow(
                doctor_comments_link, self.parse)
            request.meta["comments_class"] = "table.rates.doctor_rates_preview tr"

            yield request

    def parse_comment(self, comment_division, url):
        id = self.comment_id(comment_division)
        avg_rate = comment_division.css(".avg_rate::text").extract_first()
        avg_text = comment_division.css(".avg_text::text").extract_first()
        datetime = comment_division.css(".datetime::text").extract_first()

        content = self.filtered_content(comment_division, "p.comment2")

        if not content:
            content = self.filtered_content(comment_division, "p.comment")

        pos_content = self.filtered_content(
            comment_division, "p.comment_plus")

        neg_content = self.filtered_content(
            comment_division, "p.comment_minus")

        institution_id = self.institution_id(url)
        institution_name = self.institution_name
        institution_city = self.institution_city

        author_name = comment_division.css(
            "div[itemprop=author]::text").extract_first()
        author_operator = comment_division.css(
            ".mobile_operator_img::attr(alt)").extract_first()

        moderator_reply_divisions = comment_division.css(".moder div")

        reply = self.moderator_reply(moderator_reply_divisions)

        reply_datetime = comment_division.css(
            ".moder .datetime::text").extract_first()

        doctor_name = comment_division.css(
            "div[style='float: right']::text").extract_first()

        doctor_name = self.filtered_doctor_name(doctor_name)

        return InstitutionComment(
            id=id,
            url=url,
            avg_rate=avg_rate,
            avg_text=avg_text,
            content=content,
            pos_content=pos_content,
            neg_content=neg_content,
            datetime=datetime,
            institution_id=institution_id,
            institution_name=institution_name,
            institution_city=institution_city,
            author_name=author_name,
            author_operator=author_operator,
            reply=reply,
            reply_datetime=reply_datetime,
            doctor_name=doctor_name
        )

    def comment_id(self, comment_division):
        id = comment_division.css(
            "div[data-rtype='simple']::attr(data)").extract_first()

        if id:
            return int(id)

        return int(comment_division.css(
            "div[data-rtype='detail']::attr(data)").extract_first())

    def filtered_content(self, comment_division, content_type_class):
        content = comment_division.css(content_type_class).extract_first()

        if content and remove_tags(content):
            return remove_tags(content)

    def filtered_doctor_name(self, name):
        if name:
            return " ".join(name.strip().split(" ")[2:])

    def moderator_reply(self, moder_divisions):
        if moder_divisions:
            reply_strings = moder_divisions[-1].css("::text").extract()
            return " ".join(reply_strings).strip()

    def institution_id(self, url):
        institution_id_str = url.split("/")[-3]

        if re.search("ajax", url):
            return int(institution_id_str)
        else:
            return int(institution_id_str.split("-")[0])

    def set_institution_params(self, params_div):
        self.institution_name = params_div.css(
            "div[itemprop='name']::text").extract_first().strip()

        self.institution_city = params_div.css(
            "div[itemprop='name'] div::text").extract_first().strip()

    def institutions_reviews_urls(self):
        with open('institutions.json') as institutions:
            return [institution["url"] + "otzivi/" for institution in json.load(institutions)]