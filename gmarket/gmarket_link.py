from requests import Session
from lxml import html
import csv

url = "http://browse.gmarket.co.kr/list?category=200001966&t=a&k=32&p={}"
s = Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0"
out = open("links.csv","w")
row = csv.writer(out)
for i in range(1,101):
	r = s.get(url.format(i))
	tree = html.fromstring(r.content)
	links = tree.xpath("//a[@class='link__item']/@href")
	for link in links:
		row.writerow([r.url,link])
	print(r.url)