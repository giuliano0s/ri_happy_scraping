from Utils.constants import *

import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

headers = requests.utils.default_headers()
headers.update({"User-Agent": "Chrome/51.0.2704.103"})

def URL_TEMPLATE(department, sector, page_num, min_price, max_price) -> str:
    #page starts at 1
    string_ret = f"""https://www.rihappy.com.br/{department}/{sector}
                    ?initialMap=c,c&initialQuery={department}/{sector}
                    &map=category-1,category-2&page={page_num}
                    &priceRange={min_price}%20TO%20{max_price}"""
    
    return string_ret