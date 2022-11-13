from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from lxml import html
import re
import csv


options = Options()
# options.add_argument('--headless')
driver = webdriver.Firefox(executable_path="/Volumes/Data/course5i/geckodriver",options=options)
out = open("remain_data.csv","w",newline="",encoding="utf-8")
row = csv.writer(out)



f = open("laptop_links.txt").read().split("\n")

# for i in f:
# 	driver.get(i)
# 	x = driver.page_source.replace("\n","")
# 	tree = html.fromstring(driver.page_source)
# 	battery = tree.xpath("normalize-space(//tr//td[contains(string(),'Durée de fonctionnement')]//parent::td//following-sibling::td//text())")
# 	row.writerow([i,battery])
# 	print(i)

for i in f:
	driver.get(i)
	x = driver.page_source.replace("\n","")
	tree = html.fromstring(driver.page_source)
	# mrp = "".join(tree.xpath("//div[@class='stroken']//text()"))
	mrp = "".join(re.findall('fpStriked fpStrikedAfter jsFpStrikedAfter jsStriked jsOverlay hideFromPro">(.*?)<',x)).strip()
	# price = re.findall('ion":"NewCondition","price":(.*?),',driver.page_source)
	price = ".".join(tree.xpath("//span[@class='fpPrice price jsMainPrice jsProductPrice hideFromPro']//text()"))

	name = tree.xpath("normalize-space(//h1[@itemprop='name']//text())")
	model = ""
	url = i
	p_type = tree.xpath("normalize-space(//tr//td[contains(string(),'Catégorie')]//parent::td//following-sibling::td//text())")
	
	# s_size = "".join(re.findall(' Affichage</th></tr><tr><td>Type</td><td>(.*?)<',driver.page_source))
	s_size = "".join(re.findall('Affichage</th></tr><tr><td>Type</td><td>(.*?)</td',x)) + "".join(re.findall('</tr><tr><td>Taille de la diagonale</td><td>(.*?)</td',driver.page_source))

	os = tree.xpath("//tr//td[contains(string(),'Système') and contains(string(),'exploitation')]//parent::td//following-sibling::td//text()")
	
	processor_series = tree.xpath("normalize-space(//tr//td[contains(string(),'Processeur|Fabricant') or contains(string(),'CPU')]//parent::td//following-sibling::td//text())")
	processor_model = "",
	graphics = tree.xpath("normalize-space(//tr//td[contains(string(),'Processeur graphique')]//parent::td//following-sibling::td//text())")
	hdd = tree.xpath("normalize-space(//tr//td[contains(string(),'Disque dur') or contains(string(),'Stockage principal')]//parent::td//following-sibling::td//text())")
	ram = tree.xpath("normalize-space(//tr//td[contains(string(),'RAM') and(not(contains(string(),'max')))]//parent::td//following-sibling::td//text())") + tree.xpath("normalize-space(//tr//td[contains(string(),'Taille installée') and(not(contains(string(),'max')))]//parent::td//following-sibling::td//text())")


	touch = tree.xpath("normalize-space(//h3[contains(string(),'Ecran tactile')]//parent::td//following-sibling::td//a//text())")
	resolution = tree.xpath("normalize-space(//th[contains(string(),'Affichage')]//following::tr//td[contains(string(),'Résolution')]//parent::td//following-sibling::td//text())") + "".join(re.findall('</tr><tr><td>Résolution native</td><td>(.*?)</td',driver.page_source))
	backlit = "".join(tree.xpath("//tr//td[contains(string(),'Rétroéclairage du clavier')]//parent::td//following-sibling::td//text()"))
	warrenty = tree.xpath("normalize-space(//tr//td[contains(string(),'Garantie')]//parent::td//following-sibling::td//text())")
	seller = "",
	stock = "".join(tree.xpath("//p[@class='fpProductAvailability']//text()")).strip()
	battery = tree.xpath("normalize-space(//tr//td[contains(string(),'Durée de fonctionnement')]//parent::td//following-sibling::td//text())")
	block_data = "".join(tree.xpath("//div[@id='descContent']//text()|//ul[@class='listebulletpoint']//text()|//div[@id='fpBulletPointReadMore']//text()"))

	row.writerow([mrp,price,name,model,url,p_type,s_size,os,processor_series,processor_model,graphics,hdd,ram,touch,resolution,backlit,warrenty,seller,stock,battery,block_data])
	print(i)

