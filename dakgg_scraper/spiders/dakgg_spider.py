from re import search

from urllib.parse import urlparse
from w3lib.html import remove_tags

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field
from scrapy.selector import Selector


class DakggSpider(CrawlSpider):
    name = 'dakgg_spider'
    
    start_urls = ["https://dak.gg/bser/routes"]
    allowed_domains = ["dak.gg"]

    visited_urls = set()

    def __init__(self, **kwargs):

        # Enables overriding attributes for a flexible spider
        if kwargs.get("start_urls"):
            self.start_urls = kwargs.get("start_urls")
            self.allowed_domains = list(
                urlparse(x).hostname for x in self.start_urls
            )

        super().__init__(
            **{k: v for k, v in kwargs.items() if not hasattr(self, k)}
        )

    rules = [  # Get all links on start url
        Rule(
            link_extractor=LinkExtractor(
                allow=r"bser\/routes\?character"
            ),
            follow=False,
            callback="parse_start_url"
        )
    ]

    def parse_start_url(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.add(response.url)
            print('URL IS THIS: ', response.url)
            return self.parse_weapons(response)

    def parse_page(self, response):
        header = response.css("h1, h2").extract_first() or response.css("title").extract_first() or response.url
        return {
            "character": remove_tags(header),
            "url": response.url,
        }

    def parse_images(self,response):
        items = []
        for image in response.css('img'):
            if 'bser/images/assets/character' in image.attrib['src']:
                newItem = {
                    "character": image.attrib['alt'],
                    "url": image.attrib['src'],
                }
                if newItem not in items:
                    items.append(newItem)
            else:
                if ('bser/images/assets/' in image.attrib['src']):
                    #print('VALUE : ', image)
                    pass
        return items

    def parse_weapons(self,response):
        items = []
        for route_li_entry in response.xpath("//ul[@class='route-weapon-types']/li/a"):
            newItem = {
                "character": response.url.split('=')[1],
                "weapon": search('weaponType\=(.+[^\&])', route_li_entry.attrib['href']).group(1),
                "url": route_li_entry.attrib['href'],
            }
            if newItem not in items:
                items.append(newItem)
        return items