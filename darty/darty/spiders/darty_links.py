import scrapy
import json
from scrapy.http import FormRequest

from scrapy.http import JsonRequest

class DartyLinksSpider(scrapy.Spider):
    name = 'darty_links'
    # allowed_domains = ['darty.com']
    def start_requests(self):
        data = {'TechnicalForm.SiteMapNodeId': '228394',
         'TechnicalForm.DepartmentId': '1070992',
         'TechnicalForm.ProductId': '',
         'hdnPageType': 'ProductList',
         'TechnicalForm.ContentTypeId': '3',
         'TechnicalForm.SellerId': '',
         'TechnicalForm.PageType': 'PRODUCTLISTER',
         'TechnicalForm.LazyLoading.ProductSheets': 'False',
         'TechnicalForm.BrandLicenseId': '0',
         'TechnicalForm.OriginalHash': '#_his_',
         'SortForm.BrandLicenseSelectedCategoryPath': '',
         'SortForm.SelectedSort': 'PERTINENCE',
         'ProductListTechnicalForm.Keyword': '',
         'ProductListTechnicalForm.TemplateName': 'InLine'}

         # 1070849

        # url = "https://www.darty.com/nav/achat/informatique/ordinateur_bureau/bureau/filtre_{}__pc_avec_ecran_integre__1358957.html"
        # url = "https://www.darty.com/nav/achat/informatique/ordinateur_bureau/bureau/filtre_{}__unite_centrale__1358955.html"
        #url = "https://www.darty.com/nav/achat/informatique/ordinateur_bureau/imac/page{}.html"
        # url = "https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/page{}.html"
        
        # url = "https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable_hybride/page{}.html"
        # url = "https://www.darty.com/nav/achat/informatique/ordinateur/marque_{}__microsoft__MSOFT.html"
        # url = "https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/filtre__chromebook__1553550.html#dartyclic=X_info-et-gami_pc-port-macb_chro"
        # url = "https://www.darty.com/nav/achat/informatique/macbook_imac_ipad/macbook/page{}.html"
        
        # url = "https://www.darty.com/nav/achat/informatique/ordinateur/marque__microsoft__MSOFT.html"
        #url = "https://www.fnac.com/Tous-les-ordinateurs-portables/Ordinateurs-portables/nsh154425/w-4?PageIndex={}&sl"

        # url = "https://www.amazon.de/s?rh=n%3A340843031%2Cn%3A%21340844031%2Cn%3A427957031&page={}&qid=1605634246&ref=lp_427957031_pg_{}"
        
        # url = "https://www.amazon.de/s?i=computers&bbn=427957031&rh=n%3A340843031%2Cn%3A340844031%2Cn%3A427957031&page={}&__mk_de_DE=%C3%85M%C3%85Z%C3%95%C3%91&_encoding=UTF8&field-feature_four_browse-bin=7472570031&pf_rd_i=427957031&pf_rd_m=A3JWKAKR8XB7XF&pf_rd_p=787663787&pf_rd_p=ba5440ea-eb7b-49e9-b3a3-00a8dc08caef&pf_rd_r=1519PQEDTA1TFNGS9MHN&pf_rd_r=HANSK9DQ99T8SW445NKV&pf_rd_s=merchandised-search-top-4&pf_rd_s=visualsn_de_pc-content-1&pf_rd_t=101&pf_rd_t=SubnavFlyout&qid=1605634779&ref=sr_pg_{}" #78
        
        # url = "https://www.lenovo.com/de/de/search/facet/query/v3?ch=1841299381&categories=LAPTOPS&page={}&pageSize=20&sort=sortBy&currency=EUR"

        # url = "https://www.lazada.sg/shop-laptops/lenovo/?page={}&ppath=31027%3A61474"
        # url = "https://www.lazada.sg/shop-desktop-computer/lenovo/?ajax=true&page={}&ppath=31027:61474"
        # url=["https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-portable-657?page={}&sort=ventes&view=list","https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-de-bureau-658?page={}&sort=ventes&view=list"]

        # url = "https://www.amazon.de/s?rh=n%3A340843031%2Cn%3A%21340844031%2Cn%3A427954031&page={}&qid=1605634935&ref=lp_427954031_pg_{}"

        # url = "https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-portable-657?page={}&sort=ventes&view=list"
        #url = "https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-de-bureau-658?page={}&sort=ventes&view=list"
        # url = "https://www.fnac.com/Unite-centrale/Selections-Fnac/nsh353913/w-4?PageIndex={}&sl"
        
        # url = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/l-1070992.html#_his_"
        # url = "https://www.cdiscount.com/ProductListUC.mvc/UpdateJsonPage?page={}"
        # "https://www.darty.com/nav/achat/informatique/ordinateur_bureau/page{}.html":1691,
        # url = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/l-1070992.html#_his_"
        # url = {"https://www.darty.com/nav/achat/informatique/ordinateur_bureau/bureau/filtre_{}__pc_gamer__367962.html":18,"https://www.darty.com/nav/achat/informatique/ordinateur_bureau/bureau/filtre_{}__unite_centrale__1358955.html":58}
        # 83
        # 1691

        # data["data"]


        urls = {"https://www.darty.com/nav/achat/informatique/ordinateur_bureau/bureau/filtre_{}__pc_gamer__367962.html":43,"https://www.darty.com/nav/achat/informatique/ordinateur_bureau/bureau/filtre_{}__unite_centrale__1358955.html":98,"https://www.darty.com/nav/achat/informatique/ordinateur_bureau/bureau/filtre__pc_avec_ecran_integre__1358957.html":2,"https://www.darty.com/nav/extra/list?flag=NEW_ITEM&cat=12434":2}

        ######------------------cdiscount-------------
        # url = "https://www.cdiscount.com/ProductListUC.mvc/UpdateJsonPage?page={}"
        # data["TechnicalForm.SiteMapNodeId"] = 228394
        # data["TechnicalForm.DepartmentId"] = 1070992
        # for num in range(1,306):
        #     yield JsonRequest(url=url.format(num),data=data,callback=self.parse,meta={"proxy":"http://scraperapi.country_code=de:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"})
        #----------------------cdiscount-----------

        for url in urls:
            for i in range(1,urls[url]):
                yield scrapy.Request(url = url.format(i),callback=self.parse,meta={"proxy":"http://scraperapi.country_code=fr:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"})

        # for i in url:
        #     # yield scrapy.http.FormRequest(url = url.format(i),formdata=data,callback=self.parse)
        #     # yield scrapy.Request(url = url.format(i),meta={"proxy":"http://scraperapi.country_code=de:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"},callback = self.parse,headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36","Content-Type":"application/json","Referer":"https://www.lenovo.com/de/de/d/desktop-by-Specs?sort=sortBy&currentResultsLayoutType=grid","Host":"www.lenovo.com","X-Requested-With":"XMLHttpRequest"})
        #     for num in range(1,url[i]+1):
        #         yield scrapy.Request(url=i.format(num),callback=self.parse,meta={"proxy":"http://scraperapi.country_code=de:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"})
        #     # yield JsonRequest(url = url.format(i),method="GET",callback=self.parse,meta={"proxy":"http://scraperapi.country_code=fr:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"},headers={ "Host":"www.lazada.sg","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Referer":"https://www.lazada.sg/shop-desktop-computer/lenovo/?page=2&ppath=31027%3A61474","path":"/shop-laptops/lenovo/?ajax=true&page=16&ppath=31027:61474","upgrade-insecure-requests":"1","x-umidtoken":"T2gAUXDN5j3O0AVqIW7WSSiwrM9DJLIQAMj23TKwzOs_7OX65j3M8gItlvqQ_5hssCaAm-XL_skgzAs0-bu4NRBK","X-CSRF-TOKEN":"e36b4beb1d035"})

    def parse(self, response):
        # print(response.text)
        # try:
        # data = json.loads(response.text)
        # for i in data["mods"]["listItems"]:
        #     yield{
        #         "link":i["productUrl"],
        #         "url":response.url
        #     }
        # except:
        #     print("again....")
        #     yield JsonRequest(url = response.url,method="GET",callback=self.parse,meta={"proxy":"http://scraperapi.country_code=sg:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001"},headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"})
            

        links = response.xpath("//div[@class='prd-family']//a/@href").extract() #darty
        for i in links:
            yield{
                "url":response.url,
                "link":i
            }
        # links = response.xpath("//p[@class='Article-desc']//a/@href").extract() #fnac
        

        # try:
        #     js = json.loads(response.text)

        #     # links = response.xpath("//a[@class='a-link-normal a-text-normal']/@href").extract() #amazon
        #     # title = response.xpath("//a[@class='a-link-normal a-text-normal']//span//text()").extract() #amazon
        #     # links = response.xpath("//section[@class='list']//article//a/@href").extract() #reducommerce
        #     for i in js["results"]:
        #         yield{
        #             "url":response.url,
        #             "links":response.urljoin(i["url"])
        #         }
        # except:
        #     yield{
        #         "url":response,
        #         "links":" ".join(response.xpath("//div[@class='error-content']//p//text()").extract())
        #     }

        # for j,i in zip(title,links):
        # 	yield{
        # 		"url":response.url,
        # 		"links": i,
        #         "title":j
        # 	}



        # cdiscount--------------------------------
        # js = json.loads(response.text)
        # for i in js["products"]:
        #     if(not i.get("AdBlock")):
        #         yield{
        #             "url":response.url,
        #             "links":i["urlToRedirect"]    
        #         }
                