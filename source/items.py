# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # name, brand name, image, price and category
    type = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    long_desc = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    seller = scrapy.Field()
    sku = scrapy.Field()
    url = scrapy.Field()
    availability = scrapy.Field()
    level1 = scrapy.Field()
    level2 = scrapy.Field()
    level3 = scrapy.Field()


class PortAnetItem(scrapy.Item):
    # name, brand name, image, price and category
    name = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    brand = scrapy.Field()
    affiliate_link = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    website = scrapy.Field()
    long_desc = scrapy.Field()
