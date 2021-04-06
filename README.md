# dakgg-data-loader
Loads the top rated saved plans for each character and loads them into a datastore

# Steps
> cd scripts

- follow the readme there

## Running single spider

> scrapy crawl dakgg_spider --output "feed/%(name)s-%(time)s.json" --output-format json

## Chaining multiple spiders

> python3 main.py chained_crawl dakgg_characters_spider,dakgg_routes_spider --output "feed/%(name)s-%(time)s.json" --output-format json
