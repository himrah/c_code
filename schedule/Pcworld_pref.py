from requests import Session
from bs4 import BeautifulSoup as BS
import json
import csv
import time
from lxml import html
import mysql.connector
import pandas as pd
# from loguru import logger

s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"

output = open("pl_crawl.csv","w",encoding="utf-8",newline="\n")
xl = csv.writer(output)
con = mysql.connector.connect(host="localhost",user="root",passwd="nixis123",db="local",charset="utf8", use_unicode=True)
# con = mysql.connector.connect(host="localhost",user="course5i_1",passwd="Course5@234",db="emea_commercial",charset="utf8", use_unicode=True)
cursor = con.cursor()

def api_builder(url):
     api_url = 'http://api.scraperapi.com/?api_key=a6438ab03fee3e0af7053fbbcaa5c20c&country_code=de&url='+str(url)
     return api_url

def request(url,loop = 0):
    try:
        r = s.get(api_builder(url))
        return r
    except Exception as e:
        if("Connection aborted" in str(e) and loop <5):
            request(url,loop+1)
            # print(e)
        else:
            pass
# @logger.catch
def Crawl_Link(url,retailer,category):
    global xl
    try:
        r = request(url)
        print(url)
        try:
            data  = json.loads(r.content)
            js = True
        except:
            js = False

        if(js):
            soup = BS(data["results"],'html.parser')
            description = soup.find_all("div","col-product-description-spec")
            pricing = soup.find_all("div","col-product-price-info")
            for desc,pr in zip(description,pricing):
                product_name = desc.find("a").text.strip()
                product_url = "https://business.currys.co.uk"+desc.find("a").get("href")
                markdown_price = pr.find("span","price").find("strong").text
                list_price = pr.find("span","price").find("span").text
                product_code = desc.find("small").text.split(" /")[0]
                ext_date = time.strftime("%Y-%m-%d")
                ext_time = time.strftime("%H:%M:%S")

                # xl.writerow([product_url,product_name,markdown_price,list_price,r.status_code,time.strftime("%Y-%m-%d %H:%M:%S")])
                query = "select * from pcworld_pref where product_url = '{}' and extraction_date like '{}%'".format(product_url,time.strftime("%Y-%m-%d"))
                cursor.execute(query)
                if(not cursor.fetchone()):
                    query = "insert into pcworld_pref(retailer,category,product_url,product_name,markdown_price,list_price,response_status,extraction_date)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    values = (retailer,category,product_url,product_name,markdown_price,list_price,r.status_code,time.strftime("%Y-%m-%d %H:%M:%S"))
                    cursor.execute(query,values)
                    con.commit()
                cursor.execute("select * from pl_master where retailer = '{}' and product_code='{}'".format(retailer,product_code))
                if(not cursor.fetchone()):
                    query = "insert into pl_master(retailer,category,DATE,TIME,LANDING_PAGE_URL,PRODUCT_TITLE,PRODUCT_LINK,PRODUCT_CODE,CUSTOMIZED_URL,NEW_URL,DEACTIVATED,REACTIVATED)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    values = (retailer,category,ext_date,ext_time,url,product_name,product_url,product_code,"","","","")
                    cursor.execute(query,values)
                    con.commit()
                                
            tree = html.fromstring(data["pagination"])
            if(tree.xpath("//li//strong//ancestor::li/following-sibling::li[1]//a/@href")):
                url ="https://business.currys.co.uk"+"".join(tree.xpath("//li//strong//ancestor::li/following-sibling::li[1]//a/@href"))
                Crawl_Link(url)
        else:
            soup = BS(r.content,'html.parser')
            description = soup.find_all("div","col-product-description-spec")
            pricing = soup.find_all("div","col-product-price-info")
            for desc,pr in zip(description,pricing):
                product_url = "https://business.currys.co.uk"+desc.find("a").get("href")
                product_name = desc.find("a").text.strip()
                markdown_price = pr.find("span","price").find("strong").text
                list_price = pr.find("span","price").find("span").text
                # xl.writerow([product_url,product_name,markdown_price,list_price,r.status_code,time.strftime("%Y-%m-%d %H:%M:%S")])

                product_code = desc.find("small").text.split(" /")[0]
                ext_date = time.strftime("%Y-%m-%d")
                ext_time = time.strftime("%H:%M:%S")

                query = "select * from pcworld_pref where product_url = '{}' and extraction_date like '{}%'".format(product_url,time.strftime("%Y-%m-%d"))
                cursor.execute(query)
                if(not cursor.fetchone()):
                    query = "insert into pcworld_pref(retailer,category,product_url,product_name,markdown_price,list_price,response_status,extraction_date)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    values = (retailer,category,product_url,product_name,markdown_price,list_price,r.status_code,time.strftime("%Y-%m-%d %H:%M:%S"))
                    # print(values)
                    cursor.execute(query,values)
                    con.commit()
                cursor.execute("select * from pl_master where retailer = '{}' and product_code='{}'".format(retailer,product_code))
                if(not cursor.fetchone()):
                    query = "insert into pl_master(retailer,category,DATE,TIME,LANDING_PAGE_URL,PRODUCT_TITLE,PRODUCT_LINK,PRODUCT_CODE,CUSTOMIZED_URL,NEW_URL,DEACTIVATED,REACTIVATED)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    values = (retailer,category,ext_date,ext_time,url,product_name,product_url,product_code,"","","","")
                    cursor.execute(query,values)
                    con.commit()               
            tree = html.fromstring(str(soup.find("ul","pagination")))
            if(tree.xpath("//li//strong//ancestor::li/following-sibling::li[1]//a/@href")):
                url = "https://business.currys.co.uk"+"".join(tree.xpath("//li//strong//ancestor::li/following-sibling::li[1]//a/@href"))
                Crawl_Link(url,retailer,category)
    except:
        pass

#urls = ["https://business.currys.co.uk/catalogue/computing/desktops/windows-desktops?from=main-menu","https://business.currys.co.uk/catalogue/computing/desktops/imac-mac-mini?from=main-menu","https://business.currys.co.uk/catalogue/computing/tablets/tablet?from=main-menu","https://business.currys.co.uk/catalogue/computing/laptops/windows-laptop?from=midlvlcat&heat=txt","https://business.currys.co.uk/catalogue/computing/laptops/macbook?from=main-menu","https://business.currys.co.uk/catalogue/computing/laptops/chromebook?from=main-menu"]

df = pd.read_excel("pcworld_input.xlsx")
categories = df["Category"]
retailers = df["Retailer"]
urls = df["Landing Page URL"]

for url,retailer,category in zip(urls,retailers,categories):
    Crawl_Link(url,retailer,category)