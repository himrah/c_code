from requests import Session
from bs4 import BeautifulSoup as BS
import json
import csv
import time
import pandas as pd
from lxml import html
import re
import mysql.connector
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"

# output = open("pdp_crawl.csv","w",encoding="utf-8",newline="\n")
# xl = csv.writer(output)
con = mysql.connector.connect(host="localhost",user="course5i_1",passwd="Course5@234",db="emea_commercial",charset="utf8", use_unicode=True)
# server_con = mysql.connector.connect(host="50.23.233.39",user="crawler1",passwd="data@123server",db="emea_commercial",charset="utf8", use_unicode=True)

# con = mysql.connector.connect(host="localhost",user="root",passwd="root",db="crawling",charset="utf8", use_unicode=True)
cursor = con.cursor(dictionary=True)

def api_builder(url):
    api_url = 'http://api.scraperapi.com/?api_key=a6438ab03fee3e0af7053fbbcaa5c20c&country_code=uk&url='+str(url)
    return api_url

def request(url):
    r = s.get(api_builder(url))
    return r


def Crawl(url,category,landing_page_url):
    r = request(url)
    soup = BS(r.content,'html.parser')
    specs = soup.find("div",id="specifications")
    attributes = dict(zip([i.text for i in specs.find_all("dt")],[i.text for i in specs.find_all("dd")]))
    input_attr = {}
    for j in specs.find_all("h3"):
        if(j.text == "Input"):
            ss = j.next_sibling.next_sibling
            input_attr = dict(zip([i.text for i in ss.find_all("dt")],[i.text for i in ss.find_all("dd")]))
            break
    try:
        product_name = soup.find("div",id="product-container").find("h1").text.strip()
    except:
        product_name = ""
    try:
        actual_price = soup.find("div","price-fix-no").text.strip()
    except:
        actual_price = ""
    try:
        list_price = soup.find("div","price-fix-vat").text.strip()
    except:
        list_price = ""
    brand = "".join(re.findall('manufacturer":"(.*?)",',str(r.content)))
    try:
        product_code = soup.find("input",id='code').get("value")
    except:
        product_code = "".join(re.findall('productSKU":"(.*?)",', str(r.content)))

    EAN = attributes.get("EAN")
    part_number = attributes.get("Manufacturer's Part Number")
    product_type = attributes.get("Product Type")
    os = attributes.get("Operating System")
    processor = attributes.get("Processor")
    RAM = attributes.get("Memory")
    storage = attributes.get("Storage")
    graphics = attributes.get("Graphics")
    display = attributes.get("Display")
    camera = attributes.get("Camera")
    resolution = attributes.get("Resolution")
    sound = attributes.get("Sound")
    input_type = input_attr.get("Type")
    input_feature = input_attr.get("Features")
    wireless = attributes.get("Wireless")
    dimensions = attributes.get("Dimensions (WxDxH)")
    weight = attributes.get("Weight")
    security = attributes.get("Security")
    software_included = attributes.get("Software Included")
    warrenty = attributes.get("Service & Support")
    block_data = soup.find("div",id="description").text + soup.find("div",id="specifications").text




    values = [landing_page_url,category,brand,product_name,product_code,url,list_price,actual_price,os,processor,RAM,storage,graphics,display,camera,
    resolution,wireless,dimensions,weight,warrenty,block_data,part_number
    ]
    query = "insert into pcworld_pdp_crawl(start_url,category,brand,product_name,product_code,product_url,list_price,actual_price,operating_system,processor,ram,storage,graphics,screen_size,camera,resolution,wireless,dimension,weight,warrenty,block_data,manufacture_no) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,values)
    con.commit()


# f = open("Pcworld.txt","r",encoding="utf-8").read().split("\n")
s_server = con.cursor(dictionary=True)
s_server.execute('select category,product_link,landing_page_url from pl_master where retailer="pcworldbusiness"')
rows = s_server.fetchall()
print(len(rows))

for row in rows:
    category = row["category"]
    product_link = row["product_link"]
    landing_page_url = row["landing_page_url"]
    cursor.execute("select * from pcworld_pdp_crawl where product_url = '{}'".format(product_link))
    if(not cursor.fetchone()):
        Crawl(product_link,category,landing_page_url)
        print(product_link)
    # print(i)