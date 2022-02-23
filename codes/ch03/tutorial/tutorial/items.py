# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    time = scrapy.Field()
    category = scrapy.Field()
    grade = scrapy.Field()
    pass