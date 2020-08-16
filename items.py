# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    company_field = scrapy.Field()
    company_stage = scrapy.Field()
    company_size = scrapy.Field()
    company_website = scrapy.Field()
    job_name = scrapy.Field()
    job_salary = scrapy.Field()
    job_tempt = scrapy.Field()
    job_overlook = scrapy.Field()
    job_descript = scrapy.Field()
    job_location = scrapy.Field()





