import scrapy

class RueducommerceSpider(scrapy.Spider):
	name = "rueducommerce_spider"
	def start_requests(self):
		# urls = open("laptop.txt","r").read().split()
		# urls = ["https://www.noon.com/uae-en/flexible-phone-holder-and-mount-black/N14379782A/p?o=ac1e42b7e66e46aa"]
		
		# urls={"https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-portable-657?page={}&sort=ventes&view=list":35,"https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-de-bureau-658?page={}&sort=ventes&view=list":221}
		urls={"https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-portable-657?page={}&sort=ventes&view=list":3}
		for url in urls:
			for i in range(1,urls[url]+1):
				if(urls[url] == 35):
					category = "laptop"
				else:
					category = "desktop"
				yield scrapy.Request(url = url.format(i), callback=self.parse,meta={"category":category,'proxy':"http://scraperapi.country_code=fr:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"})

	def parse(self,response):
		
		urls = response.xpath("//a[@class='item__image']/@href").getall()
		for url in urls:
			yield scrapy.Request(url="https://www.rueducommerce.fr"+url,callback=self.parse_details,meta={ 'category':'laptop','proxy':"http://scraperapi.country_code=fr:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"})
    
     
	def sentize(self,txt):
		if(len(set([i.strip() for i in txt]))==1):
			return txt[0].strip().replace("\n","")
		else:
			return " ".join(list(set([i.strip() for i in txt])))

	def parse_details(self, response):
		# translator = Translator()

		# if(response.xpath("//div[@id='aplus_feature_div']//text()")):
		#     blkdata = "".join(response.xpath("//div[@id='aplus_feature_div']/*[not(style)]//text()")).strip().replace("\n","").strip()
		# else:
		#     blkdata = ""
		# # blkdata = ' '.join(response.xpath("//section[@id='wm_section_body']//text()").getall()).replace("\n"," ").replace("\r"," ").replace("\t"," ").strip()

		# blkdata = response.xpath("//div[@id='aplus_feature_div']//text()").getall()
		# blkdata = self.sentize(response.xpath("""//section[@id='wm_section_body']//text()""").getall()),
		blkdata = " ".join(response.xpath("""//section[@id='wm_section_body']//text()""").getall()),
		Block = ' '.join(response.xpath("//ul[@class='liste-attibutes']//text()").getall()).strip(),
		# if(blkdata):
		#     blkdata = "".join(response.xpath("//div[@id='aplus_feature_div']//text()")).strip().replace("\n","").strip()
		# else:
		#     blkdata = ""

		yield{
				'competitor_list_price':self.sentize(response.xpath("//div[@class='prix-conseille']//span//text()").getall()),

				'competitor_markdown_price': self.sentize(response.xpath("""//div[@class='price main']//span[@class='prix-final-formate']/@data-prix-final""").getall()),
				
			
				'competitor_product_id': self.sentize(response.xpath("""//meta[@itemprop='sku']/@content""").getall()),
				
				'competitor_product_name':self.sentize(response.xpath("""//div[@class='titreDescription']//h1//span[@itemprop='name']//text()""").getall()), 
				
				'competitor_model': '',
				'competitor_product_url':response.url,
				'competitor_laptop_type': "laptop",

				# 'competitor_screen_size': " ".join(response.xpath('//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Taille de l")]//following-sibling::td//text()|//tr//span[@class="a-size-base a-text-bold" and contains(string(),"Display Size")]/ancestor::td//following-sibling::td//text()').getall()),
				

				'competitor_screen_size':self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'Taille standard ')]//following-sibling::div//text() |//div[contains(@class,"spec-title") and contains(string(),"Diagonale d'écran d'ordinateur")]//following-sibling::div//text() | //div[contains(@class,"spec-title") and contains(string(),"Taille d'écran")]//following-sibling::div//text() | //div[contains(@class,"spec-title") and contains(string(),"d'écran")]//following-sibling::div//text()""").getall()),




				'competitor_operating_system': self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),"Version du Système d'exploitation")]//following-sibling::div//text() | //div[contains(@class,'spec-title') and contains(string(),"Type de Système d'exploitation")]//following-sibling::div//text() | //div[contains(@class,'spec-title') and contains(string(),"d'exploitation")]//following-sibling::div//text()""").getall()),
				
				



				#' '.join(response.xpath('//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Système d")]//following-sibling::td//text()|//tr//span[@class="a-size-base a-text-bold" and contains(string(),"Système ")]/ancestor::td//following-sibling::td//text()').getall()),

				
				
				# 'competitor_processor_series':" ".join(response.xpath('//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"processeur")]//following-sibling::td//text() | //li//span[@class="a-list-item" and contains(string(),"Processeur")]//text()').getall()).replace("\n","").strip(),
				'competitor_processor_series' : self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'Modèle du processeur portable')]//following-sibling::div//text()|//div[contains(@class,'spec-title') and contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'processeur')]//following-sibling::div//text()""").getall()),
				
				# Processeur
				# //div[contains(@class,'spec-title') and contains(string(),'Modèle du processeur portable')]//following-sibling::div//text()|//div[contains(@class,'spec-title') and contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'processeur')]//following-sibling::div//text()

				
				'competitor_processor_model': "",
				# self.sentize(response.xpath("""//td//span[@class='a-size-base a-text-bold' and contains(string(),"Numéro du modèle")]/ancestor::td//following-sibling::td//span[@class='a-size-base']//text() | //th[@class='a-color-secondary a-size-base prodDetSectionEntry' and contains(string(),"Numéro du modèle")]//following-sibling::td//text()""").getall())
				
				# 'competitor_graphics': " ".join(response.xpath('//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"graphique")]//following-sibling::td//text()').getall()),


				'competitor_graphics' : self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'graphique')]//following-sibling::div//text()""").getall()),

				# 'competitor_harddrive_capacity':" ".join(response.xpath('//li//span[@class="a-list-item" and contains(string(),"Stockage ")]//text()').getall()),
				'competitor_harddrive_capacity':self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'Capacité totale')]//following-sibling::div//text() | //div[contains(@class,'spec-title') and contains(string(),'Capacité Disque Dur (HDD)')]//following-sibling::div//text() | //div[contains(@class,'spec-title') and contains(string(),'Capacité Disque Dur')]//following-sibling::div//text()""").getall()),


				'competitor_ram_capacity': self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'Mémoire vive installée')]//following-sibling::div//text() | //div[contains(@class,'spec-title') and contains(string(),'Mémoire')]//following-sibling::div//text()""").getall()),
				
				# " ".join(response.xpath('//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Mémoire maximale")]//following-sibling::td//text() | //tr//span[@class="a-size-base a-text-bold" and contains(string(),"Memory Size")]/ancestor::td//following-sibling::td//text()').getall()),


				#38725
				#

				'competitor_touchscreen': self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'Ecran tactile')]//following-sibling::div//text()""").getall()),
				
				'competitor_display_resolution' : self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'pixels')]//following-sibling::div//text()|//div[contains(@class,'spec-title') and contains(string(),'Résolution')]//following-sibling::div//text()""").getall()),

				# 'competitor_display_resolution': response.xpath(u"(//span[contains(string(),'Résolution')]//following-sibling::div//span[contains(string(),'pixels')])[2]//text()|//td[contains(string(),'Résolution')]//following-sibling::td[contains(string(),'pixels')]//text()|//span[contains(string(),'Résolution')]//following-sibling::div//span[contains(string(),'pixels')]//text()").get(),
				
				'competitor_optical_drive': self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'Lecteur/Graveur')]//following-sibling::div//text() | //div[contains(@class,'spec-title') and contains(string(),'Lecteur')]//following-sibling::div//text()""").getall()),
				
				'competitor_keyboard_backlit': self.sentize(response.xpath("""//div[contains(@class,'spec-title') and contains(string(),'Rétroéclairage')]//following-sibling::div//text()""").getall()),
				
				'competitor_warranty': self.sentize(response.xpath("""//div[@class='warranty']//text()""").getall()),
				
				'seller_name': "",
				'stock':"",
				'block_data':blkdata,
				"block":Block
			}