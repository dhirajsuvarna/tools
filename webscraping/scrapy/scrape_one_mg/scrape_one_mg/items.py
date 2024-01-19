# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugInfoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    marketer = scrapy.Field()
    salt_composition = scrapy.Field()
    storage = scrapy.Field()
    product_introduction = scrapy.Field()


class DrugSummaryItem(scrapy.Item):
    name = scrapy.Field()
    page_link = scrapy.Field()
    price = scrapy.Field()
    prescription_rqd_txt = scrapy.Field()
    packaging_info = scrapy.Field()
    manufacturer = scrapy.Field()
    content = scrapy.Field()
    page_no = scrapy.Field()
