import scrapy
import re
import mysql.connector
import json
import time


class ElCrawlSpider(scrapy.Spider):
	def __init__(self):
		self.conn = mysql.connector.connect(host="167.172.117.127", user="crawler@web", passwd="data@server", db="system_pfv_latam",charset="utf8", use_unicode=True)
		self.cursor = self.conn.cursor(dictionary=True)

	name = 'el_crawl'
	allowed_domains = ['elpalaciodehierro.com']
	start_urls = ['http://elpalaciodehierro.com/']



	def start_requests(self):
		urls = {"https://www.elpalaciodehierro.com/electronica/computadoras/laptops/":"laptop","https://www.elpalaciodehierro.com/electronica/tablets/tablets/":"tablets","https://www.elpalaciodehierro.com/electronica/computadoras/computadoras-de-escritorio/":"computer"}
		for url in urls:
			yield scrapy.Request(url,callback=self.parse_links,meta={"category":urls[url]})

	def parse_links(self,response):
		next_page = response.xpath("//button[@class='g-button_1 m-flex']/@data-url").get()
		links = response.xpath("//a[@class='b-product_tile-image']/@href").extract()
		# skus = response.xpath("//div[@class='b-product']/@data-pid").extract()
		# titles = response.xpath("//a[@class='b-product_tile-name']//text()").extract()
		# soup = BS(response.body,'html.parser')



		# for d in soup.find_all("div","b-product_price-old"):
		# 	d.decompose()

		# prices = [j.text.strip() for j in soup.find_all("span","b-product_price-value")]

		# for link,sku,title,price in (links,skus,titles,prices):
		products = response.xpath("//div[@class='b-product']/@data-analytics").extract()
		for product,link in zip(products,links):
			js = json.loads(product)["product"]
			print(js)
			sku = js["id"]
			price = js["price"]
			mrp = js["metric1"]
			title = js["name"]
			brand = js["brand"]
			superCategory = js["category"]
			subCategory = js["dimension18"]

			url = response.urljoin(link)
			main_page = response.url
			# price = 
			# yield scrapy.Request(url,callback=self.parse_details,meta={"main_page":main_page,"category":response.meta["category"],"SKU":sku,"brand":brand,"category_link":response.url,"superCategory":superCategory,"subCategory":subCategory})
			# yield scrapy.Request(url,callback=self.parse_details,meta={"main_page":main_page,"category":response.meta["category"],"SKU":sku,"brand":brand,"category_link":response.url,"superCategory":superCategory,"subCategory":subCategory})
			self.cursor.execute("select * from mx_elpalaciodehierro_cat_latest where sku={}".format(sku))
			if not self.cursor.fetchone():
				query = "insert into mx_elpalaciodehierro_cat_latest(Country,Category_Link,Model_Name,Model_Number,SKU,Sales_Price,Extraction_Date,Reviews_Count,Promotions,Retailer,Additional_offers_1,Brand,Category,Regular_Price,Discount,Supercategory,Product_Link,Subcategory,status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				values = ("MX",response.url,title.strip(),"",sku,price,time.strftime("%Y-%m-%d"),"","","Elpalaciodehierro","",brand,response.meta["category"],mrp,mrp-price,superCategory,url,subCategory,2)
				self.cursor.execute(query,values)
				self.conn.commit()
				yield scrapy.Request(url,callback=self.parse_details,meta={"main_page":main_page,"category":response.meta["category"],"SKU":sku,"brand":brand,"category_link":response.url,"superCategory":superCategory,"subCategory":subCategory})


		# print(".................")
		# print(next_page)
		# print(".................")
		if(next_page):
			yield scrapy.Request(next_page,callback=self.parse_links,meta={"category":response.meta["category"],"proxy":"http://scraperapi.country_code=mx:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"})
		# self.conn.close()
	def parse_details(self,response):
		name = response.xpath("//meta[@itemprop='name']/@content").get()
		price = response.xpath("//meta[@itemprop='lowPrice']/@content").get()
		discounted_price = response.xpath("//meta[@itemprop='highPrice']/@content").get()
		processor = "".join(re.findall('Procesador - (.*?)</',response.text))
		os = "".join(re.findall('Sistema Operativo - (.*?)</',response.text))
		display = response.xpath("//span[contains(string(),'Pulgadas Display')]//following-sibling::span//text()").get()
		resolution = "".join(re.findall('Resolución - (.*?)</',response.text))
		ram = "".join(re.findall('Memoria Ram - (.*?)</',response.text))
		storage = "".join(re.findall('Disco Duro - (.*?)</',response.text))
		graphics = response.xpath("//span[contains(string(),'Especificaciones Técnicas')]//following-sibling::span//text()").get()
		warrenty = response.xpath("//span[contains(string(),'Especificaciones Técnicas')]//following-sibling::span//text()").get()

		meta = response.meta
		print("----------")
		print(meta["category"])
		print("----------")
		query = "insert into mx_elpalaciodehierro_details(Country,Retailer,Brand,category_link,product_link,Model_Name,Model_Number,SKU,Regular_Price,Sales_Price,Processor,Processor_Type,Processor_Speed,Operating_System,Display,Display_Size,Display_Resolution,Display_Type,Memory,Memory_Size,Memory_Type,Hard_Drive,HDD_Type,HDD_Size,Graphics,camera,bluetooth,warranty,battery,colour,Extraction_Date,status,Series,Product_Description,Details,Project,Supercategory,Unit_price,Promotions,Additional_Offers_1,MPN,Category,Subcategory,Discount,Operating_Version,Other_All) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		values = ("MX","Elpalaciodehierro",meta["brand"],meta["category_link"],response.url,name,"",meta["SKU"],price,discounted_price,processor,processor,processor,os,display,display,resolution,display,ram,ram,ram,storage,storage,storage,graphics,"","",warrenty,"","",time.strftime("%Y-%m-%d"),"2","","","","",meta["superCategory"],discounted_price,"","","",meta["category"],meta["subCategory"],float(discounted_price)-float(price),"","")
		self.cursor.execute(query,values)
		self.conn.commit()
		yield {
			"company":"elpalaciodehierro",
			"product":response.meta["category"],
			"series":"",
			"brand":response.xpath("//h2//text()").get().strip(),
			"part_number":"",
			"country":"MX",
			"chassis":"",
			"main_page":response.meta["main_page"],
			"navigate_second":response.url,
			"lenovo_chassis":"",
			"navigate_add_to_cart":"",
			"model_name":name,
			"price":price,
			"discounted_price":discounted_price,
			"discount":"",
			"processor":processor,
			"operating system":os,
			"display":display,
			"memory":ram,
			"hard drive":storage,
			"graphics":graphics,
			"camera":"",
			"bluetooth":"",
			"warrenty":warrenty,
			"battery":"",
		}

    	






