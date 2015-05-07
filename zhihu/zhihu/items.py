# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field



class ZhihuTopicItem(Item):
   layer = Field()
   name = Field()
   id = Field()
   parent_id = Field()
   child_ids = Field()


