import sys
import json

from crawl import chained_crawl

from twisted.internet import reactor

def main():
    chained_crawl(spiders_names='dakgg_characters_spider,dakgg_routes_spider', spider_kwargs={})
    reactor.run() # the script will block here until the last crawl call is finished

main()
