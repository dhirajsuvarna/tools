# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeOneMgItem(scrapy.Item):
    # define the fields for your item here like:
    drug_name = scrapy.Field()
    marketer = scrapy.Field()
    salt_composition = scrapy.Field()
    storage = scrapy.Field()
    product_introduction = scrapy.Field()
