from requests import Session
import json
import time
import time
import mysql.connector
import concurrent.futures

s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
con = mysql.connector.connect(host="localhost",user="root",passwd="nixis123",db="crawling",charset="utf8", use_unicode=True)
cursor = con.cursor(dictionary=True)


def Crawl(row):
    category = row["category"]
    product_link = row["product_url"]
    landing_page_url = row["start_url"]
    product_code = row["product_code"]

    url = "https://www.fastshop.com.br/wcs/resources/v5/products/byPartNumber/{}".format(product_code)
    print(url)
    r = s.get(url)
    js = json.loads(r.content)
    # regular_price = js["priceOffer"]
    # discounted_price = js["priceTag"]
    if(not js.get("errorCode") == 404):
        name = js['shortDescription']
        # seller = ""
        manufacturer = js['manufacturer']
        try:
            seller = js["marketPlaceText"]
        except:
            seller = "FastShop"
        query = "insert into fastshop_pdp(date,retailer,country,LOB,category,start_url,product_name,product_url,product_code,product_model,seller,manufacturer) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (time.strftime("%Y-%m-%d"),"Fastshop","BR",category,category,landing_page_url,name,product_link,product_code,"",seller,manufacturer)
        cursor.execute(query,values)
        con.commit()
        print(row)


cursor.execute('select category,product_url,start_url,product_code from pl_master_new where retailer="Fastshop"')
rows = cursor.fetchall()
for row in rows:
#     category = row["category"]
#     product_link = row["product_url"]
#     landing_page_url = row["start_url"]
#     product_code = row["product_code"]
    Crawl(row)
#     print(product_link)
# print("start processor")
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # list(executor.map(Crawl,rows))
