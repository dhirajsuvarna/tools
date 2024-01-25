from typing import Iterable
import scrapy
from scrapy.http import Request
from scrape_one_mg.items import DrugInfoItem
from scrape_one_mg.extractors import *


class DrugsSpider(scrapy.Spider):
    name = "single_drug"
    start_urls = ["https://www.1mg.com/drugs/ivepred-4-tablet-13015"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], meta={"playwright": True})

    def parse(self, response):
        drug_item = DrugInfoItem()
        with open("sample.html", "w", encoding="utf-8") as oFile:
            oFile.write(response.text)

        drug_item = extract(response)
        yield drug_item
