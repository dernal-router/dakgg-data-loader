import json
from datetime import datetime, timedelta
import logging

def run_crawlers(event, context):
    result = []
    for x in filter(should_crawl, get_crawler_config()):
        try:
            lambda_launch_response = launch_lambda(dict(
                    spider_name=x.get("spider_name"),
                    spider_kwargs=x.get("spider_kwargs"),
                ), {})
                result.append(lambda_launch_response)
        except Exception:
            logging.exception(
                f"Could not launch spider {x.get('spider_name')}"
            )
    return result

def get_crawler_config():
    return [
        {
            "spider_name": "dakgg_spider",
            "spider_kwargs": {
                "start_urls": ["https://dak.gg/bser/routes"],
            },
            "previous_crawl": {
                "success_state": True,
                "items_crawled": 100,
                "finish_date": datetime.now() - timedelta(days=1),
            },
        }
    ]

def should_crawl(x):
    previous_crawl = x.get("previous_crawl")
    if previous_crawl:
        time_interval_hours = x.get("crawl_interval_hours", 24*7)
        return previous_crawl.get("finish_date") + timedelta(hours=time_interval_hours) < datetime.now() or not previous_crawl.get("success_state")
    return True
