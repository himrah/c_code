from lxml import html
from bs4 import BeautifulSoup as BS
from requests import Session
import json
import time
import csv

s = Session()
s.headers["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0"
links = open("nlink.txt","r").read().split()

output = open("Laptop_output.csv","w",newline="",encoding="utf-8")
row = csv.writer(output)

for link in links:
	product_id = link.split(".")[-2]
	r = s.get(link)
	tree = html.fromstring(r.text)
	title = ''.join(tree.xpath('//div[@class="product-h1-container-v2 visible-lg-block visible-xl-block"]//h1//text()')).strip()
	brand = "".join(tree.xpath("//div[@class='spec-name col-xs-6 col-md-5 col-lg-4' and contains(string(),'Brand')]//following-sibling::div//text()"))
	processer = "".join(tree.xpath("//div[@class='spec-name col-xs-6 col-md-5 col-lg-4' and contains(string(),'Processor')]//following-sibling::div//text()"))
	generation = "".join(tree.xpath("//div[@class='spec-name col-xs-6 col-md-5 col-lg-4' and contains(string(),'Generation')]//following-sibling::div//text()"))
	model = "".join(tree.xpath("//div[@class='spec-name col-xs-6 col-md-5 col-lg-4' and contains(string(),'Model')]//following-sibling::div//text()"))
	SKU = ''.join(tree.xpath('//span[@itemprop="sku"]//text()'))



	review_first_page_url = "https://api.bazaarvoice.com/data/batch.json?passkey=bai25xto36hkl5erybga10t99&apiversion=5.5&displaycode=2070_2_0-en_us&resource.q0=products&filter.q0=id%3Aeq%3A{}&stats.q0=reviews&filteredstats.q0=reviews&filter_reviews.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&resource.q1=reviews&filter.q1=isratingsonly%3Aeq%3Afalse&filter.q1=productid%3Aeq%3A{}&filter.q1=contentlocale%3Aeq%3Aen_CA%2Cen_US&sort.q1=relevancy%3Aa1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors%2Cproducts%2Ccomments&filter_reviews.q1=contentlocale%3Aeq%3Aen_CA%2Cen_US&filter_reviewcomments.q1=contentlocale%3Aeq%3Aen_CA%2Cen_US&filter_comments.q1=contentlocale%3Aeq%3Aen_CA%2Cen_US&limit.q1=8&offset.q1=0&limit_comments.q1=3&resource.q2=reviews&filter.q2=productid%3Aeq%3A{}&filter.q2=contentlocale%3Aeq%3Aen_CA%2Cen_US&limit.q2=1&resource.q3=reviews&filter.q3=productid%3Aeq%3A{}&filter.q3=isratingsonly%3Aeq%3Afalse&filter.q3=issyndicated%3Aeq%3Afalse&filter.q3=rating%3Agt%3A3&filter.q3=totalpositivefeedbackcount%3Agte%3A3&filter.q3=contentlocale%3Aeq%3Aen_CA%2Cen_US&sort.q3=totalpositivefeedbackcount%3Adesc&include.q3=authors%2Creviews%2Cproducts&filter_reviews.q3=contentlocale%3Aeq%3Aen_CA%2Cen_US&limit.q3=1&resource.q4=reviews&filter.q4=productid%3Aeq%3A{}&filter.q4=isratingsonly%3Aeq%3Afalse&filter.q4=issyndicated%3Aeq%3Afalse&filter.q4=rating%3Alte%3A3&filter.q4=totalpositivefeedbackcount%3Agte%3A3&filter.q4=contentlocale%3Aeq%3Aen_CA%2Cen_US&sort.q4=totalpositivefeedbackcount%3Adesc&include.q4=authors%2Creviews%2Cproducts&filter_reviews.q4=contentlocale%3Aeq%3Aen_CA%2Cen_US&limit.q4=1&callback=BV._internal.dataHandler0"

	#replace 100419064
	r = s.get(review_first_page_url.format(product_id,product_id,product_id,product_id,product_id))
	rv = []
	reviews = json.loads(r.text.replace("BV._internal.dataHandler0(","").replace(")",""))
	for i in reviews["BatchedResults"]["q1"]["Results"]:
		rv.append(
					{
						"review_text":i["ReviewText"],
						"verify":len(i["Badges"]),
						"time":i["LastModeratedTime"],
						"title":i["Title"],
						"rating":i["Rating"],
						"YES":i["TotalPositiveFeedbackCount"],
						"NO":i["TotalNegativeFeedbackCount"]
					}
			)
	review_count = reviews["BatchedResults"]["q0"]["Results"][0]["TotalReviewCount"]
	
	# review_count - 8

	if(review_count>8):
		for i in range(8,review_count+1,30):
			url = "https://api.bazaarvoice.com/data/batch.json?passkey=bai25xto36hkl5erybga10t99&apiversion=5.5&displaycode=2070_2_0-en_us&resource.q0=reviews&filter.q0=isratingsonly%3Aeq%3Afalse&filter.q0=productid%3Aeq%3A{}&filter.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&sort.q0=relevancy%3Aa1&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors%2Cproducts%2Ccomments&filter_reviews.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&filter_comments.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&limit.q0=30&offset.q0={}&limit_comments.q0=3".format(product_id,i)
			# print(url)
			r = s.get(url)
			reviews = json.loads(r.text)
			for j in reviews["BatchedResults"]["q0"]["Results"]:
				rv.append(
							{
								"review_text":j["ReviewText"],
								"verify":len(j["Badges"]),
								"time":j["LastModeratedTime"],
								"title":j["Title"],
								"rating":j["Rating"],
								"YES":j["TotalPositiveFeedbackCount"],
								"NO":j["TotalNegativeFeedbackCount"]
							}
						)


	for i in rv:
		row.writerow([
			time.strftime("%Y-%m-%d %H:%M:%S"),
			"Costco",
			"",
			link,
			title,
			brand,
			processer,
			generation,
			model,
			SKU,
			i["title"],
			i["verify"],
			i["review_text"],
			i["time"],
			i["rating"],
			i["YES"],
			i["NO"]
			])
	print(link)


# next_page_review_url = "https://api.bazaarvoice.com/data/batch.json?passkey=bai25xto36hkl5erybga10t99&apiversion=5.5&displaycode=2070_2_0-en_us&resource.q0=reviews&filter.q0=isratingsonly%3Aeq%3Afalse&filter.q0=productid%3Aeq%3A100419064&filter.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&sort.q0=relevancy%3Aa1&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors%2Cproducts%2Ccomments&filter_reviews.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&filter_comments.q0=contentlocale%3Aeq%3Aen_CA%2Cen_US&limit.q0=30&offset.q0=8&limit_comments.q0=3"



# data = {'passkey': 'bai25xto36hkl5erybga10t99',
#  'apiversion': '5.5',
#  'displaycode': '2070_2_0-en_us',
#  'resource.q0': 'reviews',
#  'filter.q0': ['isratingsonly:eq:false',
#   'productid:eq:100419064',
#   'contentlocale:eq:en_CA,en_US'],
#  'sort.q0': ['relevancy:a1'],
#  'stats.q0': 'reviews',
#  'filteredstats.q0': 'reviews',
#  'include.q0': 'authors,products,comments',
#  'filter_reviews.q0': 'contentlocale:eq:en_CA,en_US',
#  'filter_reviewcomments.q0': 'contentlocale:eq:en_CA,en_US',
#  'filter_comments.q0': 'contentlocale:eq:en_CA,en_US',
#  'limit.q0': '30',
#  'offset.q0': '8',
#  'limit_comments.q0': '3',
#  'callback': 'bv_351_19057'}

# x = json.loads(r.text.replace("bv_351_19057(","").replace("})","}"))