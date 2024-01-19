from typing import Iterable
import scrapy
from scrapy.http import Request
from scrape_one_mg.items import DrugInfoItem


class DrugsSpider(scrapy.Spider):
    name = "drugs"
    start_urls = ["https://www.1mg.com/drugs/ivepred-4-tablet-13015"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], meta={"playwright": True})

    def parse(self, response):
        drug_item = DrugInfoItem()
        with open("sample.html", "w", encoding="utf-8") as oFile:
            oFile.write(response.text)

        # get the drug headers
        name_of_drug = response.css("div#drug_header h1::text").get()
        drug_item["drug_name"] = name_of_drug

        drug_headers = response.css("div#drug_header div.DrugHeader__meta___B3BcU")
        for drug_header in drug_headers:
            title = drug_header.css("div.DrugHeader__meta-title___22zXC::text").get()
            if title.lower() == "marketer":
                value = drug_header.css(
                    "div.DrugHeader__meta-value___vqYM0 a::text"
                ).get()
                drug_item["marketer"] = value
            elif title.lower() == "salt composition":
                value = drug_header.css(
                    "div.DrugHeader__meta-value___vqYM0 a::text"
                ).get()
                drug_item["salt_composition"] = value
            else:
                value = drug_header.css(
                    "div.DrugHeader__meta-value___vqYM0::text"
                ).get()
                drug_item["storage"] = value

        product_introduction = response.css(
            "div#overview div.DrugOverview__content___22ZBX::text"
        ).get()

        drug_item["product_introduction"] = product_introduction
        yield drug_item
