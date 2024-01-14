from typing import Iterable
import scrapy
from scrapy.http import Request


class DrugsSpider(scrapy.Spider):
    name = "drugs"
    start_urls = ["https://www.1mg.com/drugs/ivepred-4-tablet-13015"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], meta={"playwright": True})

    def parse(self, response):
        with open("sample.html", "w", encoding="utf-8") as oFile:
            oFile.write(response.text)

        # print(response.text)
        yield {"url": "url"}
        # marketer = response.css('div.DrugHeader__meta-title___22zXC::text')
