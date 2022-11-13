from numpy import product
from requests import Session
from bs4 import BeautifulSoup as BS
import json
import csv
import time
import pandas as pd
from lxml import html
import mysql.connector
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
# con = mysql.connector.connect(host="localhost",user="crawler@web",passwd="data@server",db="emea_commercial",charset="utf8", use_unicode=True)
con = mysql.connector.connect(host="localhost",user="root",passwd="nixis123",db="crawling",charset="utf8", use_unicode=True)
cursor = con.cursor()


def Crawl_Link_Desk(landing,cat,url,retailer,id_,index):
    print(index)
    r = s.get(url.format(index))
    # r = s.get(url.format(id_,index))
    js = json.loads(r.text)
    if(r.status_code == 404):
        return True
    print(r.url)
    if(js.get('products')):
    # try:
        for i in js['products']:
            # product_link = "https://www.fastshop.com.br/web/p/d/{}/{}".format(i['partNumber'],i['shortDescription'].replace(" ","-").replace("(","").replace(")","").lower())
            product_link = i["url"]
            Product_title = i['name']
            product_code = i['id']
            query = "insert into fastshop_br(retailer,country,LOB,category,start_url,product_name,product_url,product_code)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (retailer,'BR',cat,cat,landing,Product_title,product_link,product_code)
            cursor.execute(query,values)
            con.commit()
            cursor.execute("select * from pl_master_new where retailer = '{}' and product_code='{}'".format(retailer,product_code))
            if(not cursor.fetchone()):
                query = "insert into pl_master_new(retailer,country,LOB,category,start_url,product_name,product_url,product_code)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (retailer,'BR',cat,cat,landing,Product_title,product_link,product_code)
                cursor.execute(query,values)
                con.commit()
        Crawl_Link(landing,cat,url,retailer,id_,index+1)

def Crawl_Link(landing,cat,url,retailer,id_,index):
    print(index)
    r = s.get(url.format(id_,index))
    # r = s.get(url.format(index))
    js = json.loads(r.text)
    if(r.status_code == 404):
        return True
    print(r.url)
    if(js.get('products')):
    # try:
        for i in js['products']:
            product_link = "https://www.fastshop.com.br/web/p/d/{}/{}".format(i['partNumber'],i['shortDescription'].replace(" ","-").replace("(","").replace(")","").lower())
            Product_title = i['shortDescription']
            product_code = i['partNumber']
            query = "insert into fastshop_br(retailer,country,LOB,category,start_url,product_name,product_url,product_code)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (retailer,'BR',cat,cat,landing,Product_title,product_link,product_code)
            cursor.execute(query,values)
            con.commit()
            cursor.execute("select * from pl_master_new where retailer = '{}' and product_code='{}'".format(retailer,product_code))
            if(not cursor.fetchone()):
                query = "insert into pl_master_new(retailer,country,LOB,category,start_url,product_name,product_url,product_code)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (retailer,'BR',cat,cat,landing,Product_title,product_link,product_code)
                cursor.execute(query,values)
                con.commit()
        Crawl_Link(landing,cat,url,retailer,id_,index+1)
            
df = pd.read_excel("fastshop_input.xlsx")
urls = df["Start_url"].to_list()
category = df["Category"].to_list()
retailers = df["Retailer"].to_list()
for url1,cat1,retailer1 in zip(urls,category,retailers):
    id1 = url1.split("/")[-2]
    api_url1 = "https://www.fastshop.com.br/wcs/resources//v1/products/byFilters/{}?pageNumber={}"
    # api_url1 = "https://fastshop-v6.neemu.com/searchapi/v3/search?apiKey=fastshop-v6&secretKey=7V0dpc8ZFxwCRyCROLZ8xA==&terms=desktop&page={}"
    print("------------------")
    Crawl_Link(url1,cat1,api_url1,retailer1,id1,1)
    # print(x)