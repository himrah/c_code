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
# con = mysql.connector.connect(host="localhost",user="crawler@web",passwd="data@server",db="emea_commercial",charset="utf8", use_unicode=True)
# con = mysql.connector.connect(host="localhost",user="root",passwd="root",db="crawling",charset="utf8", use_unicode=True)
con = mysql.connector.connect(host="localhost",user="course5i_1",passwd="Course5@234",db="emea_commercial",charset="utf8", use_unicode=True)
cursor = con.cursor(dictionary=True)


def api_builder(url):
    api_url = 'http://api.scraperapi.com/?api_key=a6438ab03fee3e0af7053fbbcaa5c20c&country_code=de&url='+str(url)
    return api_url


def request(url):
    r = s.get(api_builder(url))
    return r

def Crawl(url,category,landing_page_url):
    r = request(url)
    soup = BS(r.content,'html.parser')
    tree = html.fromstring(r.content)
    # specs = soup.find('form',id='conteneurCheckboxFiche')
    

    try:
        product_name = "".join(tree.xpath("//meta[@property='og:title']//@content")).strip()
    except:
        product_name = ""
    try:
        actual_price = "".join(tree.xpath("//div[@class='tab delivery']//span[@class='oldPrice']//text()")).strip()
    except:
        actual_price = ""
    try:
        list_price = "".join(tree.xpath("//div[@class='tab delivery']//div[contains(@class,'price ')]//text()")).strip()
    except:
        list_price = ""
    brand = ""
    try:
        product_code = "".join(tree.xpath("//div[@class='productID']/@data-product-id"))
    except:
        product_code = "".join(re.findall("pdp/(.*?)/",url)).upper()

    try:
        os = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Betriebssystem')]/parent::tr//p//text()")).strip()
    except:
        os = ""
    try:
        processor = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Prozessor')]/parent::tr//p[contains(string(),'Prozessor')]//text()"))
    except:
        processor = ""
    try:
        RAM = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Arbeitsspeicher')]/parent::tr//p[contains(string(),'DDR')]//text()"))
    except:
        RAM = ""
    try:
        storage = ''.join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Festplatte')]/parent::tr//p//text()"))
    except:
        storage = ""
    try:
        graphics = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Grafik')]/parent::tr//p[contains(string(),'Grafik')]//text()|//td[@class='detailTitle' and contains(string(),'Grafik')]/parent::tr//p[contains(string(),'Graphics')]//text()"))
    except:
        graphics = ""
    try:
        display = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Display')]/parent::tr//p[contains(string(),'Zoll')]//text()"))
    except:
        display = ""

    weight = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Gewicht')]/parent::tr//p//text()")).strip()
    dimensions = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Abmessungen')]/parent::tr//p//text()")).strip()
    try:
        wireless = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Kommunikation')]/parent::tr//p[2]//text()"))
    except:
        wireless = ""
    try:
        resolution = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Display')]/parent::tr//p[contains(string(),'Pixel')]//text()"))
    except:
        resolution = ""
    # try:
    #     wireless = attr["Communications"]["Sans fil"]
    # except:
    #     wireless = ""
    # try:
    #     dimensions = attr["Dimensions et poids"]["Dimensions (LxPxH)"]
    # except:
    #     dimensions = ""
    # try:
    #     weight = attr["Dimensions et poids"]["Poids"]
    # except:
    #     weight = ""
    # security = attributes.get("Security")
    # software_included = attributes.get("Software Included")
    try:
        warrenty = "".join(tree.xpath("//td[@class='detailTitle' and contains(string(),'Herstellergarantie')]/parent::tr//p[contains(string(),'Jahr')]//text()"))
    except:
        warrenty = ""
    
    block_data = '|'.join(tree.xpath("//div[@class='keyfacts']//li//text()|//td[@class='detailTitle' and contains(string(),'Besonderheiten')]/parent::tr//li//p//text()")).strip()
    battery = ','.join(tree.xpath(u"//tr//td[contains(string(),'Akku')]//following::td[1]//text()"))
    
    # laptop_type = category
    camera = ""

    values = [landing_page_url,category,brand,product_name,product_code,url,list_price,actual_price,os,processor,RAM,storage,graphics,display,camera,
    resolution,wireless,dimensions,weight,warrenty,block_data
    ]
    query = "insert into cyberport_pdp_crawl(start_url,category,brand,product_name,product_code,product_url,list_price,actual_price,operating_system,processor,ram,storage,graphics,screen_size,camera,resolution,wireless,dimension,weight,warrenty,block_data) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    # query = "insert into cyberport_de(script_name,competitor_list_price,competitor_markdown_price,competitor_product_id,competitor_product_name,competitor_model,competitor_product_url,competitor_laptop_type,competitor_screen_size,competitor_operating_system,competitor_processor_series,competitor_processor_model,competitor_graphics,competitor_harddrive_capacity,competitor_ram_capacity,competitor_touchscreen,competitor_display_resolution,competitor_optical_drive,competitor_keyboard_backlit,competitor_warranty,seller_name,stock,Block_data,battery,time_stamp)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.execute(query,values)
    con.commit()
    print(values)


# f = open("Pcworld.txt","r",encoding="utf-8").read().split("\n")
cursor.execute('select category,product_link,landing_page_url from pl_master where retailer="cyberport"')
rows = cursor.fetchall()

for row in rows:
    category = row["category"]
    product_link = row["product_link"]
    cursor.execute(f"select * from cyberport_pdp_crawl where product_url='{product_link}'")
    if not cursor.fetchone():
	    landing_page_url = row["landing_page_url"]
	    Crawl(product_link,category,landing_page_url)
	    print(product_link)
    # print(i)