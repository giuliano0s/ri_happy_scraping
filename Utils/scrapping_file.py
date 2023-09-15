from Utils.constants import *
from time import sleep

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
        products = bs.select(".vtex-product-summary-2-x-element--search-shelf")
        products = [x for x in products if ("Indisponível" not in str(x))]


        final_name_list = []
        final_price_list = []
        for product in products:
            product_name = product.select(""".vtex-product-summary-2-x-brandName""")
            try:
                product_name = product_name[0].text 
            except:
                product_name = np.nan
            final_name_list.append(product_name)

#%% Price
            product_price_int = product.select(""".vtex-product-price-1-x-currencyInteger--shelf-price-discount""")
            product_price_int = [product_price_int[x].text for x in range(len(product_price_int))]
            if len(product_price_int)>1:
                int_price = product_price_int[0]+product_price_int[1]
            else:
                int_price = product_price_int[0]

            float_price = product.select(""".vtex-product-price-1-x-currencyFraction--shelf-price-discount""")
            try:
                float_price = float_price[0].text 
            except:
                float_price = np.nan

            product_price_final = int_price+'.'+float_price
            final_price_list.append(product_price_final)

#%% SKU
        html_body = page.text
        html_sliced = html_body.split("{")
        targets = [x.replace(' ','')[10:21] for x in html_sliced if "itemId" in x]
        skus = [x[:-2] if x[-1] not in ['0123456789'] else x for x in targets]
        skus = skus[:len(final_name_list)]

        return final_name_list, final_price_list, skus
    
    def scan_num_products(self, url) -> int:
        page = requests.get(url,headers=headers)
        bs = BeautifulSoup(page.content, 'lxml')

        num_products_raw = bs.select(""".vtex-search-result-3-x-showingProductsCount""")

        if len(num_products_raw)>0:
            num_products = num_products_raw[0].text.split(" ")[-1].replace('.','')
        else:
            num_products = 0

        return int(num_products)
