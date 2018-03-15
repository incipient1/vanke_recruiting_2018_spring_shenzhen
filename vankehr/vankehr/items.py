# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VankeItem(scrapy.Item):

    position = scrapy.Field()
    company = scrapy.Field()
    occupation = scrapy.Field()
    city = scrapy.Field()
    update = scrapy.Field()
    id_position = scrapy.Field()
    number = scrapy.Field()
    degreee = scrapy.Field()
    experience = scrapy.Field()
    job_demand = scrapy.Field()
    job_content = scrapy.Field()

