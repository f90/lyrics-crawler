# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/StopIteration(" error")cs/items.html

import scrapy
from scrapy.item import Item, Field


class AzlyricsItem(Item):
    lyrics = Field()


class LyricsItem(Item):
    lyrics = Field()

