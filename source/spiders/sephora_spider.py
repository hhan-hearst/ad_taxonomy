import json
import os
import scrapy
import json
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from source.items import ProductItem
from bs4 import BeautifulSoup
import requests


class SephoraSpider(CrawlSpider):
    name = "sephora"
    custom_settings = {"IMAGES_STORE": '../images/sephora'}
    base_url = "https://www.sephora.com"
    allowed_domains = ["sephora.com"]
    start_urls = [
        "https://www.sephora.com/shop/makeup-cosmetics",
        "https://www.sephora.com/shop/skincare",
        "https://www.sephora.com/shop/fragrance",
        "https://www.sephora.com/shop/hair-products",
        "https://www.sephora.com/shop/men",
        "https://www.sephora.com/shop/bath-body",
        "https://www.sephora.com/shop/makeup-tools"
    ]

    def parse_start_url(self, response):
        base_category = response.url.split("/")[-1]
        soup = BeautifulSoup(requests.get(response.url).text)
        category_soups = soup.findAll("a", {"data-at": "top_level_category"})
        for category_soup in category_soups:
            category_url = category_soup["href"]
            category_name = category_soup.text
            new_category_url = SephoraSpider.base_url + category_url
            my_request = scrapy.Request(
                new_category_url,
                callback=self.parse_subcategory
            )
            my_request.meta["category_info"] = {
                "base_category": base_category,
                "category": category_name
            }
            yield my_request

    def parse_subcategory(self, response):
        soup = BeautifulSoup(requests.get(response.url).text)
        sub_category_soups = soup.findAll("a", {"data-at": "nth_level"})
        for sub_category_soup in sub_category_soups:
            sub_category_url = sub_category_soup["href"]
            sub_category_name = sub_category_soup.text
            sub_category_url = SephoraSpider.base_url + sub_category_url
            my_request = scrapy.Request(
                sub_category_url,
                callback=self.parse_items
            )

            my_request.meta["category_info"] = {
                "category": response.meta["category_info"]["category"],
                "base_category": response.meta["category_info"]["base_category"],
                "sub_category": sub_category_name,
            }
            yield my_request

    def parse_items(self, response):
        category = response.meta['category_info']
        soup = BeautifulSoup(requests.get(response.url, timeout=3).text)
        products = json.loads(soup.findAll("script", {"type": "application/ld+json"})[1].text)
        number_of_products = soup.find("span", {"data-at": "number_of_products"}).text
        number_of_products = "".join([s for s in number_of_products if s.isdigit()]) if number_of_products else "60"
        number_of_products = int(number_of_products)
        if number_of_products > 60:
            for i in range(2, 2 + int(number_of_products / 60)):
                my_request = scrapy.Request(
                    response.url + "?currentPage=%s" % i,
                    callback=self.parse_next_page_items
                )
                my_request.meta["category_info"] = response.meta['category_info']
                yield my_request

        for product in products:
            soup_product = BeautifulSoup(requests.get(product["url"]).text)
            long_desc = json.loads(
                soup_product.findAll("script")[19].text
            )[6]["props"]["currentProduct"]["longDescription"]
            print (long_desc)
            item = ProductItem(
                type=product["@type"],
                brand=product["brand"],
                category=product["category"],
                name=product["name"],
                long_desc=long_desc,
                price=product.get("offers", {}).get("price", "unknown"),
                seller=product.get("offers", {}).get("seller", {}).get("name", ""),
                sku=product.get("offers", {}).get("sku", ""),
                url=product["url"],
                availability=product.get("offers", {}).get("availability", ""),
                level1=category["base_category"],
                level2=category["category"],
                level3=category["sub_category"],
            )
            yield item


    def parse_next_page_items(self, response):
        category = response.meta['category_info']
        soup = BeautifulSoup(requests.get(response.url, timeout=3).text)
        products = json.loads(soup.findAll("script", {"type": "application/ld+json"})[1].text)
        number_of_products = soup.find("span", {"data-at": "number_of_products"}).text
        number_of_products = "".join([s for s in number_of_products if s.isdigit()]) if number_of_products else "60"
        number_of_products = int(number_of_products)
        for product in products:
            soup_product = BeautifulSoup(requests.get(product["url"]).text)
            long_desc = json.loads(
                soup_product.findAll("script")[19].text
            )[6]["props"]["currentProduct"]["longDescription"]
            item = ProductItem(
                type=product["@type"],
                brand=product["brand"],
                category=product["category"],
                name=product["name"],
                long_desc=long_desc,
                price=product.get("offers", {}).get("price", "unknown"),
                seller=product.get("offers", {}).get("seller", {}).get("name", ""),
                sku=product.get("offers", {}).get("sku", ""),
                url=product["url"],
                availability=product.get("offers", {}).get("availability", ""),
                level1=category["base_category"],
                level2=category["category"],
                level3=category["sub_category"],
            )
            yield item

