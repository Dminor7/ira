from ira.spider.scraper import Crawl
from typing import List, Dict
import codecs
import json


class MetaScraper(Crawl):
    """
    The class inherits the Crawl class.
    The child class include following attributes

    Attributes:
        method: str             The request method, currently only GET is supported.
        urls: list[url]         The list of URLs to be scraped.
        fields: dict            The fields to be scraped loaded from config.json file.
        proxies:Optional[dict]  The proxy containing dictionary with keys http and https.

    Currently supported config.json selection types:
        css 
        xpath
        find
        regex
        tables
    """
    method: str = "GET"
    urls: List[str] = ["https://www.technewsworld.com/perl/section/tech-blog/"]

    with open("./jobs/meta/config.json") as f:
        fields: List[Dict] = json.load(f)
    
    path = "./jobs/meta/data.json"



"""
Run the MetaScraper by calling the class method run()
"""
MetaScraper.run()
    
    

