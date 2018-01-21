# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MovieItem(Item):
    title = Field()
    movieInfo = Field()
    star = Field()
    quote = Field()

class Zhibo8Item(Item):
    title = Field()
    info = Field()
