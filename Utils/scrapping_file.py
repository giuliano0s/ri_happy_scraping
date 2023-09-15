from Utils.constants import *
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import re

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

    def URL_TEMPLATE(self, department=None, page_num=None) -> str:
        string_return = (f"""https://www.cec.com.br/{department}?page={page_num}""")
        
        return string_return
    
    def get_num_pages(self, department):
        page = requests.get(f'https://www.cec.com.br/{department}',headers=headers)
        bs = BeautifulSoup(page.content, 'lxml')
        department_url_raw = bs.findAll("a", href=f"/{department}")

        department_url = []
        for x in range(len(department_url_raw)):
            try: 
                department_url_raw[x]['class']
            except:
                department_url.append(department_url_raw[x])

        num_of_items = int(department_url[1].text.replace('(','').replace(')','').split(' ')[-1])
        num_of_pages = int(np.ceil(num_of_items/24))

        return num_of_pages#, num_of_items
    
    def get_products_list_page(self, department, page_num):

        page = requests.get(f'https://www.cec.com.br/{department}?page={page_num}',headers=headers)
        bs = BeautifulSoup(page.content, 'lxml')

        product_list = bs.select(".itemListElement")
        sku_list = bs.findAll("meta", itemprop="sku")

        return product_list, sku_list
    
    def get_product_info(self, product_list, product, department):
        
        to_remove_list = ['Utron', '  ', 'Preço por m²', ' Preço por m²', 'Portobello', 'Incefra']

        #print(product_list[product].text)
        if 'Preço por m²' in product_list[product].text:
            product_format = re.split(r'        |    |   |  |\n', product_list[product].text)
        else:
            product_format = re.split(r'        |    |   |\n', product_list[product].text)
        product_format = [x.replace('\r','') for x in product_format if len(x)>1]

        squareM_flag_list_return = 0
        for i in to_remove_list:
            if i in product_format:
                product_format.remove(i)
                if i in ['Preço por m²', ' Preço por m²']:
                    squareM_flag_list_return = 1

        try:
            float(product_format[5].replace('.','').replace('R$','').replace(',','.'))
        except:
            if 'Indisponível' not in product_format[5]:
                product_format.remove(product_format[5])

        if len(product_format)<=6:
            product_format[5] = '-1'
            product_format.append('none')


        return product_format, squareM_flag_list_return
    

    
