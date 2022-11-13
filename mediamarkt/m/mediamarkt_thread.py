from lxml import html
from bs4 import BeautifulSoup as BS
import pandas as pd
import re
import mysql.connector
import time
import json
import concurrent.futures
from requests import Session
import csv


con = mysql.connector.connect(host="localhost", user="root", passwd="root", db="crawling",charset="utf8", use_unicode=True)
cursor = con.cursor(dictionary=True)

out = open("output.csv","w",encoding="utf-8")
write = csv.writer(out)


s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"

def api_builder(url):
	 api_url = 'http://api.scraperapi.com/?api_key=a6438ab03fee3e0af7053fbbcaa5c20c&country_code=de&url='+str(url)
	 return api_url

def crawl(url):
	api_url = api_builder(url)
	print(url)
	r = s.get(api_url)
	print(r.status_code)
	soup = BS(r.content,'html.parser')
	tree = html.fromstring(r.content)
	l = []
	laptop_type = screen = os = p_series = p_model = graphics = weight = wireless = camera = hdd = ram = touch = diamension = resolution = optical = backlit = battery_life =  ""
	main = json.loads(tree.xpath("//script[@type='application/ld+json']//text()")[0])
	sku = main["sku"]
	name = main["name"]
	try:
		price = soup.find("span","BrandedPricestyled__WholePrice-sc-1r6586o-7").text
	except:
		price = ""

	mrp = "".join(re.findall('"strikePrice":(.*?),',r.text))
	try:
		data = re.search("window.__PRELOADED_STATE__ = (.*?)};",r.text).group(1)
	except:
		pass
	block = "".join(tree.xpath("//section[@id='description']//text()"))
	block2 = "".join(tree.xpath("//section[@id='features']//text()"))
	price = "".join(tree.xpath("//span[@class='Typostyled__StyledInfoTypo-sc-1jga2g7-0 cVVVZb BrandedPricestyled__WholePrice-sc-1r6586o-7 fcdpYE']//text()"))
	DOT = "".join(tree.xpath("//sup[@class='Typostyled__StyledInfoTypo-sc-1jga2g7-0 jGtcSU BrandedPricestyled__DecimalPrice-sc-1r6586o-8 PTyRR']//text()"))
	price = price+DOT                
	for i in re.findall('GraphqlProductFeature",(.*?)\}\]',data):
		l.append(json.loads("{"+i+"}]}"))
	product_name = "".join(tree.xpath("//h1//text()"))
	category = tree.xpath('//ul[@class="Breadcrumbstyled__StyledUl-sc-1xovjem-1 bmWBmp"]//li//span[@color="grey5"]//text()')[-1]
	brand = "".join(tree.xpath('//img[@class="PdpHeader__StyledManufacturerImage-sc-1xrongt-4 inTwoZ"]/@title'))
	product_code = url.split("-")[-1].replace(".html","")
	for i in l:
		if(i.get("name")):
			if(i.get("name") == "Produkttyp"):
				laptop_type = i.get("value")
			if(i.get("name")== "Bildschirmdiagonale (cm/Zoll)"):
				screen = i.get("value")
			if(i.get("name") == "Betriebssystem"):
				os = i.get("value")
			if(i.get("name") == "integrierte Webcam"):
				camera = i.get("value")

			if(i.get("name") == "Prozessor"):
				p_series = i.get("value")
			if(i.get("name")=="Prozessor-Modell"):
				p_model = i.get("value")
			if(i.get("name")=="Grafikkarte"):
				graphics = i.get("value")
			if(i.get("name")== "Festplatte 1"):
				hdd = i.get("value")
			if(i.get("name")== "WLAN"):
				wireless = i.get("value")
			if(i.get("name")=="Arbeitsspeicher-Größe"):
				ram = i.get("value")
			if(i.get("name") == "Touchscreen"):
				touch = i.get("value")
			if(i.get("name")=="Bildschirmauflösung"):
				resolution = i.get("value")
			if(i.get("name") == "Laufwerkstyp"):
				optical = i.get("value")
			if(i.get("name") == "Tastatur"):
				backlit = i.get("value")
			if(i.get("name") == "Akku-Laufzeit"):
				battery_life = i.get("value")
			if(i.get("name") == "Abmessungen (B/H/T) / Gewicht"):
				diamension = i.get("value")
			if(i.get("name") == "Gewicht (laut Hersteller)"):
				weight = i.get("value")                            
	print(url)
	values = ["",laptop_type,brand,product_name,product_code,url,mrp,price,os,p_series+p_model,ram,hdd,graphics,screen,camera,resolution,wireless,diamension,weight,'',"","NO"]
	write.writerow(values)
	print(values)
	# for i in values:
	#     print(i,type(i))
	# query = "insert into mediamarkt_pdp_crawl(start_url,category,brand,product_name,product_code,product_url,list_price,actual_price,operating_system,processor,ram,storage,graphics,screen_size,camera,resolution,wireless,dimension,weight,warrenty,block_data,refurbish) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"            
	# curosr.execute(query,values)
	con.commit()



rows = open("input.txt","r").read().split("\n")


t0 = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
	list(executor.map(crawl,rows))
t1 = time.time()
print(f"{t1-t0} seconds....")
