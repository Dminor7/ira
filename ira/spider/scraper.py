from requests_html import AsyncHTMLSession
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from functools import partial
from urllib.parse import urlparse, parse_qs
import re
from fake_headers import Headers
import pandas as pd
from fp.fp import FreeProxy
import parslepy
import lxml.etree
import random
import jsonstreams
import codecs

class Trial:
    def __enter__(self):
        pass

    def __exit__(self, *args):
        return True
trial = Trial()


class Crawl:
    """
    This is a class containing operations required for the scraper.

    Class method :
        run: Execute the child the inherited classes by calling this method
    """
    def __init__(self):
        self.asession = AsyncHTMLSession()
        retries = Retry(total=2, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504])
        self.asession.mount("http://", HTTPAdapter(max_retries=retries))
        self.asession.mount("https://", HTTPAdapter(max_retries=retries))
        self.data = []
        self.headers = Headers(headers=True)
        self.stream = jsonstreams.Stream(jsonstreams.Type.array,fd=codecs.open(self.path,"w", encoding="utf-8") , indent=4, pretty=True)
        # self.proxies = {
        #     "http":FreeProxy(anonym=True, rand=True, country_id=['US']).get()
        # }


    async def async_get(self, url):
        """
        Parameters:
            url: str The url to request for
        
        Returns:
            r: requests.Response 
        """
        headers = {
            "user-agent": self.headers.generate()["User-Agent"],
            "reffer":"https://www.google.com/"
        }
        r = None
        try:
            r = await self.asession.get(url, proxies=self.proxies, headers=headers)
        except Exception as e:
            try:
                r = await self.asession.get(url, headers=headers)
            except Exception as e:
                pass
        return r

    def get(self):
        """
        For the list of given URLs this function 
        run all the coroutines (async_get, url) it will 
        wrap each one in a task, run it and wait for the result. 
        Return a list with all results as requests.Response, this is returned in the same order coros are passed in.
        """
        if self.method.lower() == "get":
            tasks = [partial(self.async_get, url) for url in self.urls]
            responses = self.asession.run(*tasks)
            return responses

    def get_attribute(self, element, attribute):
        """
        For a given element and attribute name returns the value of attribute or None. 

        Parameters:
            element: Union[List[str], List[requests_html.Element], str, requests_html.Element]
            attribute: str
        Returns:
            value: str
        """
        value = None
        if attribute == "text":
            with trial: value = element.text.strip()
        else:
            with trial: value = element.attrs[attribute]
        return value

    def find_attribute(self, element, attribute):
        """
        For a given list of elements or element calls the get_attribute function
        Parameters:
            element: Union[List[str], List[requests_html.Element], str, requests_html.Element]
            attribute: str
        Returns:
            value: List OR str
        """
        if isinstance(element, list):
            return [self.get_attribute(ele, attribute) for ele in element]
        else:
           return self.get_attribute(element,attribute)

    def get_tables(self,html):
        """
        For the given html this function returns all tables found in the HTML

        Parameters:
            html: Unicode representation of the HTML content.
        Returns:
            tables: List[List[Dict]]
        """
        output_table = None
        with trial:
            tables = pd.read_html(html)
            output_table = [table.to_dict("records") for table in tables]
        return output_table

    def recursive_extract(self, html, rules):
        data = None
        with trial:
            html_parser = lxml.etree.HTMLParser()
            doc = lxml.etree.fromstring(html, parser=html_parser)
            p = parslepy.Parselet(rules)
            data = p.extract(doc)
        return data

    def find_field(self,response):
        """
        This function iterates over the field object for given response

        Parameters:
            response: requests.Response
        """
        result = {field["name"]:None for field in self.fields}
        if response:
            result["response_url"] = None
            result["response_status_code"] = None
            result["response_elaspsed_total_seconds"] = None
            with trial: result["response_url"] = response.url
            with trial: result["response_status_code"] = response.status_code
            with trial: result["response_elaspsed_total_seconds"] = response.elapsed.total_seconds()

            with trial: response = response.html
            for field in self.fields:
                selection = field.get("selection")
                element = None

                # Element Extraction
                if selection == "xpath":
                    for s in field.get("search"):
                        with trial: element = response.xpath(s, first=field.get("first"))
                        if element:
                            break
                
                if selection == "css":
                    for s in field.get("search"):
                        with trial: element = response.find(s, first=field.get("first"))
                        if element:
                            break
                
                if selection == "find":
                    for s in field.get("search"):
                        with trial: result[field.get("name")] = response.search(s)[0]
                    continue
                
                if selection == "regex":
                    for s in field.get("search"):
                        with trial: result[field.get("name")] = re.search(s, response.html).group(1)
                    continue
                
                if selection == "tables":
                    with trial: result[field.get("name")] = self.get_tables(response.html)
                    continue
                
                if selection == "recursive":
                    result[field.get("name")] = self.recursive_extract(response.html, field.get("rules"))
                    continue

                # Element's Attribute Extraction
                if pattern := field.get("extract_from_text"):
                    with trial: 
                        text = self.find_attribute(element,field.get("attribute"))
                        text = re.findall(pattern,text)
                        if len(text) == 1:
                            result[field.get("name")] = text[0]
                        else:
                            result[field.get("name")] = text
                
                elif pattern := field.get("extract_from_href"):
                    with trial:
                        href = self.find_attribute(element,field.get("attribute"))
                        if "?" in pattern:
                            href = urlparse(href)
                            href = parse_qs(href.query)
                            with trial: result[field.get("name")] = href.get(pattern.strip("?"))[0]
                
                else:
                    with trial: result[field.get("name")] = self.find_attribute(element,field.get("attribute"))

        # self.data.append(result)
        self.stream.write(result)
                

    def parse(self, class_name="Test"):
        """
        This method yield reponses to be parsed
        """
        responses = self.get()
        return list(map(self.find_field,responses))       

    def execute(self, class_name):
        """
        starts executing by to scrape
        """
        self.parse(class_name)
        self.stream.close()

    @classmethod
    def run(cls):
        """
        ClassMethod run 
        """
        self = cls()
        class_name = self.__class__.__name__
        print("Executing....")
        self.execute(class_name)
        return True
