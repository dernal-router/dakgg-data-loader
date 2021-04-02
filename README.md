# dakgg-data-loader
Loads the top rated saved plans for each character and loads them into a datastore

# Steps
- cd scripts
- follow the readme there
- scrapy crawl dakgg_spider --output "feed/%(name)s-%(time)s.json" --output-format json
