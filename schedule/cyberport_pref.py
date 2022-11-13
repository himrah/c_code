from requests import Session
from bs4 import BeautifulSoup as BS
import json
import csv
import time
from lxml import html
import mysql.connector
import pandas as pd
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
s.headers["Host"] = "www.cyberport.de"
s.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
s.headers["Connection"] = "keep-alive"
s.headers["Cookie"] = "_abck=C1183A2811E18FCB2B2D1C7C9190515A~0~YAAQjXxBFwgeSfB4AQAAh6I5HQV/NoYUJOgKYZgiL9/R5+OqPzUUwZk9mZsykIGP7tDzjHEjJ+PovBW9c6Lg0FnFm0cLwFDdg6k3QDeioRDQ7sBOR2BAlWo4Gosm9Hh1ZrOftgYcOPsSuEoWehek+a9ERwxmWVWNID30hSSn417/y9LxXwG/y37eSfzc6cI84khkgKy5lO+dK+3GBYLzKiXvYQmzKVDyybBVkt/hsU8NUiKkOGDzHoBcC0ruGvwKuWUdE7Bfn9RJsj8RF/0rJ3PIinRdAakXEjMseHLkGPLrHUWs/8wUTizkNLeMqM7P8R6YYZChO5Ji+kQ9Ky7hXzasBmGVW1A3b2T2p4N9MmReqiblgkI/G82zEceyIzJ1Zp3Q9uJEQEcbvzkdJXP78n4pfQr1P3BGEuW7UiFrbA45Ipc=~-1~-1~-1; retnbb=63; AMCV_FB2F5FCF5C08…_page=www.notebooksbilliger.de; _dy_csc_ses=p056759gl92tn9p3vdzm8faxebqd4exs; _dy_c_att_exps=; _gcl_au=1.1.659352466.1619693020; _gid=GA1.2.1681693655.1619693021; cto_bundle=oGkgaF9UaEJqcGF5ZHg0bjVETlpHJTJGR1dzQ0slMkZZNVlUbHZNWUVLajdjUUQlMkIlMkJnb0ZkNXBISm40czZNR2ZnOEFDUGZpNyUyQkVyQm1wVUQlMkJwJTJGcU1PSTJpaXBFN1NPTEVFSVZ4QnUyVlFpMCUyRk9EcFZNU0FaMFJGUHljSyUyRlZnT3A0YkdKSkFCSzdNalRZMVdYQ2xYZ1hlQm5Ba3MyOFdPSERMc1pnWGlTSzBJVGtFQkx5QXMlM0Q; s_sq=%5B%5BB%5D%5D; CRTOABE=0; hl_p=5df3cd5b-39b3-4bfb-8ee8-08a3dc41bca7".encode("utf-8")

# con = mysql.connector.connect(host="localhost",user="crawler@web",passwd="data@server",db="emea_commercial",charset="utf8", use_unicode=True)
con = mysql.connector.connect(host="localhost",user="course5i_1",passwd="Course5@234",db="emea_commercial",charset="utf8", use_unicode=True)
cursor = con.cursor()


def api_builder(url):
    api_url = 'http://api.scraperapi.com/?api_key=a6438ab03fee3e0af7053fbbcaa5c20c&country_code=de&url='+str(url)
    return api_url


def request(url):
    r = s.get(api_builder(url))
    return r
    # try:
    #     r = s.get(url)
    #     return r
    # except:
    #     request(url)
def Crawl_Link(url,retailer,category):
    print(url)
    r = request(url)
    soup = BS(r.content,'html.parser')
    tree = html.fromstring(r.content)
    trs = soup.find_all("article","productArticle")
    for tr in trs:
        product_url = "https://www.cyberport.de"+tr.find("a","head heading-level3").get("href")
        try:
            product_name = tr.find("a","head heading-level3").find("h3").text.strip()
        except:
            product_name = ""
        try:
            markdown_price = tr.find("div","price").text.strip()
        except:
            markdown_price = ""
        try:
            list_price = tr.find("span","oldPrice").text.strip()
        except:
            list_price = ""
        if(tr.find("span","tooltipAppend available")):
            stock = "In Stock"
        else:
            stock = "Out of Stock"
        product_code = tr.get("data-product-id")

        query = "insert into cyberport_pref(retailer,category,product_url,product_name,markdown_price,list_price,response_status,extraction_date,stock,product_code)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (retailer,category,product_url,product_name,markdown_price,list_price,r.status_code,time.strftime("%Y-%m-%d %H:%M:%S"),stock,product_code)
        cursor.execute(query,values)
        con.commit()            
    
    if("".join(tree.xpath("//div[@class='paging']//a[@class='active']/following-sibling::a[1]/@href"))):
        url = "https://www.cyberport.de" + "".join(tree.xpath("//div[@class='paging']//a[@class='active']/following-sibling::a[1]/@href"))
        Crawl_Link(url,retailer,category)
        



# def Crawl(url,retailer,category):
#     r = s.get(url)
#     soup = BS(r.content,'html.parser')
#     category_id = soup.find("input",attrs={"name":"category_id"}).get("value")
#     perPage = int(soup.find("a","item_per_page_links active").text)
#     last_page = int(soup.find("div","nbb-pagination").find_all("a")[-2].text)

#     for page_numer in range(1,last_page+1):
#         url = "https://www.notebooksbilliger.de/extensions/apii/filter.php?filters=on&listing=on&advisor=&action=applyFilters&category_id={}&page={}&perPage={}&sort=popularity&order=desc&availability=alle&eqsqid=".format(category_id,page_numer,perPage)
#         Crawl_Link(url, retailer, category)

df = pd.read_excel("cyberport_input.xlsx")
categories = df["Category"]
retailers = df["Retailer"]
urls = df["Landing Page URL"]

for url,retailer,category in zip(urls,retailers,categories):
    Crawl_Link(url,retailer,category)