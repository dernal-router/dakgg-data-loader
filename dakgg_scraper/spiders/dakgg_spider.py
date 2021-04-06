import json

from re import search

from urllib.parse import urlencode, urlparse, urlunparse, parse_qs, parse_qsl
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
                allow=r"\?character=[a-zA-Z]+",
                deny=r"make|consumable|hl|page"
            ),
            process_links="add_en_lang",
            follow=True
        ),
        Rule(
            link_extractor=LinkExtractor(
                allow=r"eyJpdiI6I.+",
            ),
            process_links="add_en_lang",
            follow=False,
            callback="parse_start_url"
        )
    ]

    def add_en_lang(self, links):

        for each_link in links:
            params = { 'hl': 'en-US' }

            url_parts = list(urlparse(each_link.url))
            query = dict(parse_qsl(url_parts[4]))
            query.update(params)

            url_parts[4] = urlencode(query)

            each_link.url = urlunparse(url_parts)

            yield each_link

    def parse_start_url(self, response):

        if response.url not in self.visited_urls:
            # self.visited_urls.add(response.url)
            print('URL IS THIS: ', response.url)
            meta = {}

            if 'eyJpdiI6I' in response.url:

                return self.parse_routes(response)
            if 'weaponType' in response.url:
                meta['character'] = parse_qs(urlparse(response.url).query)['character']
                meta['weapon'] = parse_qs(urlparse(response.url).query)['weaponType']

                return self.parse_modes(response, meta)
            elif 'character' in response.url:
                meta['character'] = parse_qs(urlparse(response.url).query)['character']

                return self.parse_weapons(response, meta)
            else:
                return self.parse_characters(response, meta)

    def parse_characters(self, response, meta={}):
        items = []
        for image in response.css('img'):
            if 'bser/images/assets/character' in image.attrib['src']:
                newItem = {
                    "character": image.attrib['alt'],
                    "url": image.attrib['src'],
                }
                if newItem not in items:
                    print('NEW CHARACTER', str(newItem))
                    # items.append(newItem)
                    pass
            else:
                if ('bser/images/assets/' in image.attrib['src']):
                    #print('VALUE : ', image)
                    pass
        return items

    def parse_weapons(self, response, meta={}):
        items = []
        for route_li_entry in response.xpath("//ul[@class='route-weapon-types']/li/a"):
            newItem = {
                "character": meta['character'][0] if 'character' in meta.keys() else 'Unknown',
                "weapon": search('weaponType\=(.+[^\&])', route_li_entry.attrib['href']).group(1),
                "url": route_li_entry.attrib['href'],
            }
            if newItem not in items:
                print('NEW WEAPON', str(newItem))
                items.append(newItem)
        return items

    def parse_modes(self, response, meta={}):
        items = []
        for route_li_entry in response.xpath("//ul[@class='route-weapon-types']/li/a"):
            newItem = {
                "character": meta['character'][0] if 'character' in meta.keys() else 'Unknown',
                "weapon": search('weaponType\=(.+[^\&])', route_li_entry.attrib['href']).group(1),
                "url": route_li_entry.attrib['href'],
            }
            if newItem not in items:
                print('NEW WEAPON', str(newItem))
                items.append(newItem)
        return items

    def parse_routes(self, response, meta={}):
        items = []
        path = []
        for route_li_entry in response.xpath('//script/text()'):
            if 'window.__route' in route_li_entry.get():
                json_s = search('window\.__route = (.+)\;', route_li_entry.get()).group(1)
                json_obj = json.loads(json_s)
                path = [ json_obj['areas'][num-1]['name'] for num in json_obj['paths']] if json_obj and 'paths' in json_obj.keys() else []
        newItem = {
            "character": response.xpath("//div[@class='route-header__character']/img").attrib['alt'],
            "weapon": response.xpath("//div[@class='route-header__weapon-type']/img").attrib['alt'],
            "path": ','.join(path),
            "url": response.url,
        }
        if newItem not in items:
            print('NEW ROUTE', str(newItem))
            items.append(newItem)
        return items
