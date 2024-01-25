# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugInfoItem(scrapy.Item):
    # define the fields for your item here like:
    headers = scrapy.Field()
    overview = scrapy.Field()
    uses = scrapy.Field()
    benefits = scrapy.Field()
    side_effects = scrapy.Field()
    how_to_use = scrapy.Field()
    how_drug_works = scrapy.Field()
    safety_advice = scrapy.Field()
    missed_dose = scrapy.Field()
    # substitutes = scrapy.Field()
    expert_advice = scrapy.Field()
    fact_box = scrapy.Field()
    drug_interaction = scrapy.Field()
    # patient_concerns = scrapy.Field()
    # user_feedback = scrapy.Field()
    faq = scrapy.Field()


class DrugSummaryItem(scrapy.Item):
    name = scrapy.Field()
    page_link = scrapy.Field()
    price = scrapy.Field()
    prescription_rqd_txt = scrapy.Field()
    packaging_info = scrapy.Field()
    manufacturer = scrapy.Field()
    content = scrapy.Field()
    page_no = scrapy.Field()
