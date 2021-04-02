#!/bin/bash
cd ..
#scrapy crawl dakgg_spider --output "feed/%(name)s-%(time)s.json" --output-format json
python3 main.py
