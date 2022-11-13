# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import codecs
import os
import hashlib
import sys
# reload(sys)
import time
# sys.setdefaultencoding('utf-8')


class PontoSpider(CrawlSpider):
    name = 'ponto'
    # allowed_domains = ['pontofrio.com.br','pdp-api.pontofrio.com.br']
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63"
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    meta = {
            'proxy': 'http://scraperapi:a6438ab03fee3e0af7053fbbcaa5c20c@proxy-server.scraperapi.com:8001'
        }
        
    #function for converting a file to array
    def file_to_array(self,n):
        # f = open(n, 'r')
        x = f.read().split("\n")
        f.close()
        return x
        
    def w_t_f(self,fname,mode,enco,str1):
        x = codecs.open(fname,mode,enco)
        x.write(str1)
        x.close
    
    def save_url(self,response):
        c_dir = os.getcwd()
        file_name = c_dir +'/html/'+ self.url_to_md5(response.url) + '.html'
        page_html = response.text
        f = open(file_name,'w')
        f.write(page_html)
        f.close()
        return file_name
    
    def url_to_md5(self,url):
        m = hashlib.md5()
        m.update(url)
        return m.hexdigest()
    
    #function for converting a file to array
    def file_to_array(self,n):
        f = open(n, 'r')
        x = f.read().splitlines()
        f.close()
        return x
     

    def start_requests(self):
        # inp = self.file_to_array("input.txt")
        # inp = open("input.txt","r").read().split("\n")
        inp = open("prd_link.txt","r").read().split("\n")
        # url = "https://www.pontofrio.com.br/c/informatica/notebook/lenovo/?filtro=c56_c57_m294"
        # inp = open("links.txt").read().split("\n")
        # yield scrapy.Request(url=url,callback=self.crawl_link1,meta={"index":1,"json":False},headers={'User-Agent': self.user_agent})
        
        for i in inp:
            # yield scrapy.Request(url='https://www.americanas.com.br/categoria/informatica/notebook/m/samsung?ordenacao=topSelling', headers={
                # 'User-Agent': self.user_agent
            # })
            yield scrapy.Request(url = i,callback=self.parse_item, headers={'User-Agent': self.user_agent},meta={"url":i})
            # yield scrapy.Request(url=i,callback=self.crawl_link,meta={"index":1,"json":False},headers={'User-Agent': self.user_agent})

    # rules = (
    #     # Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
    #     Rule(LinkExtractor(restrict_xpaths="//div[@class='lista-produto prateleira']//ul[@class='vitrineProdutos']//li//a[@class='link url']"), callback='parse_item', follow=False, process_request='set_user_agent'),
    #     # Rule(LinkExtractor(restrict_xpaths='//span[@aria-label="Next"]/parent::node()'), process_request='set_user_agent')
    #     Rule(LinkExtractor(restrict_xpaths="//li[@class='atual']/following-sibling::li[1]//a"), process_request='set_user_agent')
    # )


    # def crawl_link1(self,response):
    #     if(response.meta["json"]):
    #         print("................----")
    #         j = json.loads(response.body)
    #         if(j["products"]):
    #             # prd_links = [x["urls"] for x in j["products"]]
    #             for product in j["products"]:
    #                 link = product["urls"]
    #                 yield {"cat":response.url,"url":link}
    #                 # yield scrapy.Request(url = link,callback=self.parse_item,headers={'User-Agent': self.user_agent})
    #             next_page = "https://www.pontofrio.com.br/api/catalogo-ssr/products/?{}&PaginaAtual={}&RegistrosPorPagina=20&Platform=1".format(response.url.split("?")[1].split("&")[0],response.meta["index"]+1)
    #             # yield {"cat":response.url,"url":link}
    #             yield scrapy.Request(url = next_page,callback=self.crawl_link1, meta={"index":response.meta["index"]+1,"json":True},headers={'User-Agent': self.user_agent})
    #     else:
    #         links = response.xpath("//a[@class='styles__CardMediaWrapper-sc-1gzprri-4 iSxxlY']/@href").extract()
    #         for link in links:
    #             yield {"cat":response.url,"url":link}
    #             # yield scrapy.Request(url = link,callback=self.parse_item,headers={'User-Agent': self.user_agent})

    #         if(response.xpath("//button[@class='LoadMore__Button-orxhtv-0 jdODqO']")):
    #             next_page = "https://www.pontofrio.com.br/api/catalogo-ssr/products/?{}&PaginaAtual={}&RegistrosPorPagina=20&Platform=1".format(response.url.split("?")[1],response.meta["index"]+1)
    #             yield scrapy.Request(url = next_page, callback=self.crawl_link1, meta={"index":response.meta["index"]+1,"json":True},headers={'User-Agent': self.user_agent})        

    def crawl_link(self,response):
        if(response.meta["json"]):
            j = json.loads(response.body)
            if(j["products"]):
                # prd_links = [x["urls"] for x in j["products"]]
                for product in j["products"]:
                    link = product["urls"]
                    yield {"url":link,"cat":response.url}
                    # yield scrapy.Request(url = link,callback=self.parse_item,headers={'User-Agent': self.user_agent})
                next_page = "https://www.pontofrio.com.br/api/catalogo-ssr/products/?{}&PaginaAtual={}&RegistrosPorPagina=20&Platform=1".format(response.url.split("?")[1].split("&")[0],response.meta["index"]+1)
                yield scrapy.Request(url = next_page,callback=self.crawl_link, meta={"index":response.meta["index"]+1,"json":True},headers={'User-Agent': self.user_agent})
        else:
            links = response.xpath("//a[@class='styles__CardMediaWrapper-sc-1gzprri-4 iSxxlY']/@href").extract()
            for link in links:
                yield {"url":link,"cat":response.url}
                # yield scrapy.Request(url = link,callback=self.parse_item,headers={'User-Agent': self.user_agent})

            if(response.xpath("//button[@class='LoadMore__Button-orxhtv-0 jdODqO']")):
                next_page = "https://www.pontofrio.com.br/api/catalogo-ssr/products/?{}&PaginaAtual={}&RegistrosPorPagina=20&Platform=1".format(response.url.split("?")[1],response.meta["index"]+1)
                yield scrapy.Request(url = next_page, callback=self.crawl_link,meta={"index":response.meta["index"]+1,"json":True},headers={'User-Agent': self.user_agent})
        
    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request
    
    def clean_lb(self,st):
        j = st.split("\n")
        cd = ""
        for jj in j:
            jj = jj.strip()
            if jj != "":
                cd = cd + " " + jj
        return cd.strip()
    
    def get_data_bw(self,s,sv,ev):
        # import pdb;pdb.set_trace()
        op = ""
        j = s.find(sv)
        if not j == -1:
            k = s.find(ev,j+len(sv))
            if not k == -1:
                op = (s[j+len(sv):k]).strip()
        return op
    
    # def parse_item(self, response):    
        # fn = self.save_url(response)
        # stat = response.url + "\t" + fn + "\n"
        # self.w_t_f("stat.txt","a","utf-8",stat)
        # # import pdb;pdb.set_trace()
        # yield {
            # 'competitor_list_price': response.xpath("//p[contains(@class,'product-price-original')]//text()").get(),
            # # 'competitor_list_price': response.xpath("//strong[@id='ctl00_Conteudo_ctl00_precoDeValue']//text()").get(),
            # 'competitor_markdown_price': response.xpath("//span[@class='product-price-value']//text()").get(),
            # # 'competitor_markdown_price': response.xpath("//i[@class='sale price']//text()").get(),
            # 'competitor_product_id': response.xpath(u"//p[@class='css-1v3yibb e1o4qi6b0']//span[1]//text()").get(),
            # # 'competitor_product_id': self.get_data_bw(response.xpath(u"//span[@itemprop='productID']//text()").get(),"Item ",")"),
            # 'competitor_product_name': response.xpath("//h1//text()").get(),
            # # 'competitor_product_name': response.xpath("//b[@itemprop='name']//text()").get(),
            # # 'competitor_model': response.xpath(u"//tr[contains(@class, 'Tr-sc-1wy23hs-3 cNwYXF') and contains(.//span, 'Referência do Modelo')]/td[2]/span/text()").get(),
            # 'competitor_product_url': response.url,
            # 'competitor_laptop_type': response.xpath("normalize-space(//dl[@class='Tipo']//dd//text())").get(),
            # 'competitor_screen_size': response.xpath(u"normalize-space(//dl[ contains (@class,'Tamanho-da-tela')]//dd//text())").get(),
            # 'competitor_operating_system': response.xpath(u"normalize-space(//dl[ contains (@class,'Sistema-operacional')]//dd//text())").get(),
            # 'competitor_processor_series': response.xpath(u"normalize-space(//dl[ contains (@class,'Processador')]//dd//text())").get(),
            # # 'competitor_processor_model': "",
            # 'competitor_graphics': response.xpath(u"normalize-space(//dl[ contains (@class,'Placa-de-video')]//dd//text())").get(),
            # 'competitor_harddrive_capacity': response.xpath(u"normalize-space(//dl[ contains (@class,'Disco-rigido--HD')]//dd//text())").get(),
            # 'competitor_ram_capacity': response.xpath(u"normalize-space(//dl[ contains (@class,'Memoria-RAM')]//dd//text())").get(),
            # # 'competitor_touchscreen': "",
            # 'competitor_display_resolution': (''.join(response.xpath(u"//dl[ contains (@class,'Caracteristicas-Gerais') and contains (.//dd,'resolução')]//text()").getall())).replace("\n","").replace("\r","").strip(),
            # 'competitor_optical_drive': response.xpath(u"normalize-space(//dl[ contains (@class,'Unidade-optica')]//dd//text())").get(),
            # # 'competitor_keyboard_backlit': "",
            # 'seller_name': response.xpath("//a[@class='seller']//text()").get(),
            # 'competitor_warranty': response.xpath(u"normalize-space(//dl[ contains (@class,'Garantia')]//dd//text())").get(),
            # # 'stock': "",
            # 'Block_data': (''.join(response.xpath("//div[@id='descricao']//text()").getall())).replace("\n","").replace("\r","").strip(),
            # 'time_stamp': time.strftime("%Y-%m-%d %H:%M:%S")
        # }

    def retry(self,failure):
        meta = failure.request.meta
        print("..--------------{}---------------".format("403"))
        yield scrapy.Request(url = meta["url"],callback=self.parse_item,errback = self.retry, headers={'User-Agent': self.user_agent})


    def parse_item(self, response):
        # fn = self.save_url(response)
        # stat = response.url + "\t" + fn + "\n"
        # self.w_t_f("stat.txt","a","utf-8",stat)
        
        url = response.url
        script = ''.join(response.xpath('//script[@id="__NEXT_DATA__"]//text()').extract())
        json_data = json.loads(script)
        
        purl = response.url
        cid = json_data['query']['sku']
        pname = json_data['props']['initialState']['Product']['product']['name']
        processor= ""
        os =""
        ctype =""
        screen_size =""
        graphics =""
        HDD =""
        RAM =""
        display_resolution =""
        od=""
        warrenty =""
        block=""
        product_detail = json_data['props']["initialState"]["Product"]["product"]["description"]
        attributes = product_detail.split("<br>")
        # for attr in attributes:
        #     if(attr.lower().find("intel ")!=-1 or attr.lower().find("amd ")!=-1):
        #         processor = attr
        #     if(attr.lower().find("ram")!=-1):
        #         RAM = attr
        #     if()
        
        
        lop = json_data['props']['initialState']['Product']['product']['specGroups']
        # print(lop)
        # processor
        if lop:
            for i in range(len(lop)):
                specs = lop[i]['specs']
                for j in range(len(specs)):
                    nm = specs[j]['name']
                    if "Processador"==nm:
                        processor = specs[j]['value']
                    # else:
                    #     processor=""
                    
                    if "Sistema operacional"==nm:
                        os = specs[j]['value']
                    # else:
                    #     os=""
                        
                    if "tipo"==nm.lower():
                        ctype = specs[j]['value']
                    # else:
                    #     ctype=""
                        
                    if "Tamanho da tela"==nm:
                        screen_size = specs[j]['value']
                    # else:
                    #     screen_size=""
                        
                    if "Placa de vídeo"==nm:
                        graphics = specs[j]['value']
                    # else:
                        # graphics=""
                        
                    if "Disco rígido (HD)"==nm:
                        HDD = specs[j]['value']
                    # else:
                        # HDD=""
                        
                    if "Memória RAM"==nm:
                        RAM = specs[j]['value']
                    # else:
                        # RAM=""
                    
                    if "Características Gerais"==nm:
                        display_resolution = specs[j]['value']
                    # else:
                        # display_resolution=""
                        
                    if "Unidade óptica"==nm:
                        od = specs[j]['value']
                    # else:
                        # od=""
                        
                    if "Garantia"==nm:
                        warrenty = specs[j]['value']
                    # else:
                        # warrenty=""
                    
                    block = block + specs[j]['name'] + "|" + specs[j]['value']
        # else:
        #     for attr in attributes:
        #         if(len(attr)<70):
        #             if(attr.lower.find("intel")!=-1 or attr.lower.find("amd")!=-1):
        #                 processor = attr
        #             if(attr.lower.find("windows")!=-1 or attr.lower.find("linux")!=-1 or attr.lower.find("chrome os")!=-1):
        #                 os = attr
        #             if()
                    
                        
        jsonurl = "https://pdp-api.pontofrio.com.br/api/v2/sku/"+str(cid)+"/price/source/PF"
        yield scrapy.Request(jsonurl,callback=self.parse_details,meta={"purl":purl,"cid":cid,"pname":pname,"processor":processor,"os":os,"ctype":ctype,"screen_size":screen_size,"graphics":graphics,"HDD":HDD,"RAM":RAM,"display_resolution":display_resolution,"od":od,"warrenty":warrenty,"block":block})
    
    def parse_details(self,response):
        # if(response)
        # print(dir(response.headers))
        json_data = json.loads(response.text)
        try:
            price =json_data['sellPrice']['priceValue']
        except:
            price =""
            
        try:
            seller_name = json_data['sellers'][0]['name']
        except:
            seller_name =""
        
        if json_data['sellPrice']:
            sb =json_data['sellPrice']['showPriceBefore']
            

        print("________________________{}___________________".format(sb))
        # import pdb;pdb.set_trace()
        if sb==True or sb:
            list_price = json_data['sellPrice']['priceBefore']
        else:
            list_price=""
        # import pdb;pdb.set_trace()
        yield {
            'competitor_list_price': list_price,
            'competitor_markdown_price': price,
            'competitor_product_id': response.meta['cid'],
            'competitor_product_name': response.meta['pname'],
            'competitor_model': '',
            'competitor_product_url': response.meta['purl'],
            'competitor_laptop_type': response.meta['ctype'],
            'competitor_screen_size': response.meta['screen_size'],
            'competitor_operating_system': response.meta['os'],
            'competitor_processor_series': response.meta['processor'],
            'competitor_processor_model': "",
            'competitor_graphics': response.meta['graphics'],
            'competitor_harddrive_capacity': response.meta['HDD'],
            'competitor_ram_capacity': response.meta['RAM'],
            'competitor_touchscreen': "",
            'competitor_display_resolution': response.meta['display_resolution'],
            'competitor_optical_drive': response.meta['od'],
            'competitor_keyboard_backlit': "",
            'seller_name':seller_name,
            'competitor_warranty': response.meta['warrenty'],
            'stock': "",
            'Block_data': response.meta['block'],
            'time_stamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }

