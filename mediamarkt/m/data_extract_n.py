import mysql.connector
import pandas as pd
import time
import sys
# conn = mysql.connector.connect(host="127.0.0.1", user="root", passwd="nixis123", db="EMEA_OEM",charset="utf8", use_unicode=True)

# args = sys.argv
# print(args)

# file,retailer = sys.argv
date = time.strftime("%Y-%m-%d")
# date = time.strftime("2021-09-21")
# conn = mysql.connector.connect(host="50.23.233.39", user="crawler1", passwd="data@123server", db="oem",charset="utf8", use_unicode=True)
conn = mysql.connector.connect(host="localhost", user="root", passwd="root", db="crawling",charset="utf8", use_unicode=True)
cursor = conn.cursor(dictionary=True)

# query = 'SELECT mediamarkt.brand as retailer,mediamarkt.category,mediamarkt.brand,mediamarkt.product_code,mediamarkt.country,mediamarkt.product_url,mediamarkt.product_name,p_ref.list_price,p_ref.discounted_price,mediamarkt.processor,mediamarkt.operating_system,mediamarkt.screen_size,mediamarkt.ram,mediamarkt.storage,mediamarkt.graphics,mediamarkt.camera,mediamarkt.bluetooth,mediamarkt.warrenty,mediamarkt.battery,mediamarkt.resolution,mediamarkt.color,mediamarkt.block_data,mediamarkt.date FROM mediamarkt,p_ref where mediamarkt.product_code = p_ref.product_code  and mediamarkt.country = p_ref.country and p_ref.date like "%{}%" and brand="{}"'.format(date,retailer)
# query = 'select pref.extraction_date,pdp.product_name from mediamarkt_pref as pref,mediamarkt_pdp_crawl as pdp where pref.product_code = pdp.product_code and pref.extraction_date like "%2021-08-11%"'
query = 'select pref.extraction_date as date, pdp.category,pdp.start_url,pdp.brand,pdp.product_name,pdp.product_url,pdp.product_code,pref.markdown_price as list_price,pref.list_price as actual_price,pdp.processor,pdp.operating_system,pdp.screen_size,pdp.ram,pdp.storage,pdp.graphics,pdp.camera,pdp.bluetooth,pdp.battery,pdp.warrenty,pdp.resolution,pdp.color,pdp.dimension,pdp.weight,pdp.wireless,pdp.block_data,pdp.refurbish from mediamarkt_pref as pref,mediamarkt_pdp_crawl as pdp where pref.product_code = pdp.product_code and pref.extraction_date like "%{}%"'.format(date)
cursor.execute(query)
rows = cursor.fetchall()
df = pd.DataFrame(rows)
# df.insert(3,column="Retailer_inner",value="")
# df.insert(6,column="Chassis",value="")
# df.insert(7,column="Main_page",value="")
# df.insert(9,column="lenovo_chassis",value="")
# df.insert(10,column="navigate_add_to_cart",value="")
# df.insert(14,column="dollar_off",value="")
# df.columns = ["Retailer","Supercategory","Brand","Retailer_inner","Part_Number","Country","Chassis","Main_page","Navigation_Second","lenovo_chassis","navigate_add_to_cart","model_name","Regular_Price","Sales_Price","dollar_off","Processor","Operating_System","Display","Memory","Hard_Drive","Graphics","camera","bluetooth","warranty","battery","Display_Resolution","colour","Details","Extraction_Date"]
# df["Details"] = ""

df.to_excel("Output/{}_{}.xlsx".format("mediamarkt",date),index=False)