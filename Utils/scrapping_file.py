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
headers.update({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'})

class Scraping_Class:

    def __init__(self):
        pass

    def URL_TEMPLATE(self, department=None, sector=None, page_num=1, min_price=0, max_price=5000) -> str:
        #page starts at 1
        string_return = (f"""https://www.rihappy.com.br/{department}/{sector}?initialMap=c,c&initialQuery={department}/{sector}&map=category-1&page={page_num}&priceRange={min_price}%20TO%20{max_price}""")
        
        return string_return
    
    def scan_products(self, url) -> list:

        page = requests.get(url,headers=headers)
        bs = BeautifulSoup(page.content, 'lxml')

        products_raw = bs.select(""".vtex-product-summary-2-x-clearLink--search-shelf""")
        products_list = [x['href'] for x in products_raw]
        

        return products_list
    
    def scan_num_products(self, url) -> int:
        page = requests.get(url,headers=headers)
        bs = BeautifulSoup(page.content, 'lxml')

        num_products_raw = bs.select(""".vtex-search-result-3-x-showingProductsCount""")

        if len(num_products_raw)>0:
            num_products = num_products_raw[0].text.split(" ")[-1].replace('.','')
        else:
            num_products = 0

        return int(num_products)
    
    def get_product_info(self, url):
        page = requests.get(url,headers=headers)
        bs = BeautifulSoup(page.content, 'lxml')
        
        try:
            int_prices = bs.select(""".vtex-product-price-1-x-currencyInteger--pdp-price-discount""")
            if len(int_prices)>1:
                int_price = int_prices[0].text+int_prices[1].text
            else: 
                int_price = int_prices[0].text
                
            float_price = bs.select(""".vtex-product-price-1-x-currencyFraction--pdp-price-discount""")[0].text
            final_price = int_price+'.'+float_price
        except:
            final_price = np.nan
            print('price not found:')
            print(url)

        try:
            name = bs.select(""".vtex-store-components-3-x-productBrand """)[0].text
        except:
            print('name not found:')
            print(url)
            name = np.nan

        try:
            sku = bs.select(""".vtex-product-identifier-0-x-product-identifier__value""")[0].text
        except:
            print('sku not found:')
            print(url)
            sku = np.nan

        return final_price, name, sku