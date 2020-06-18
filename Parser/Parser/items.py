# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IdnesItem(scrapy.Item):
    link = scrapy.Field()
    header = scrapy.Field()
    category = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    opener = scrapy.Field()
    paragraphs = scrapy.Field()
    comments = scrapy.Field()
    image = scrapy.Field()


class IdnesCommentItem(scrapy.Item):
    name = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
