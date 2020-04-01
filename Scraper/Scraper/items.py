# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScraperItem(scrapy.Item):
    article_title = scrapy.Field()
    article_url = scrapy.Field()
    article_author = scrapy.Field()
    comments_count = scrapy.Field()
    published = scrapy.Field()
    category = scrapy.Field()
    paragraphs = scrapy.Field()
    tags = scrapy.Field()

    pass

