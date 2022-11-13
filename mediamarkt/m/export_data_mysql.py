import mysql.connector
import pandas as pd
import time
import os
retailer = "cdiscount"
date = time.strftime("%d%m%Y")

try:
    os.mkdir("pdp_output/{}".format(date))
except:
    pass

# server_con = mysql.connector.connect(host="50.23.233.39",user="crawler1",passwd="data@123server",db="emea_commercial",charset="utf8", use_unicode=True)
con = mysql.connector.connect(host="localhost", user="root", passwd="root", db="crawling",charset="utf8", use_unicode=True)
cursor = con.cursor(dictionary=True)
# server_cursor = server_con.cursor(dictionary=True)
# server_cursor.execute("select * from pl_master where retailer ='{}'".format(retailer))

# server_cursor.execute("SELECT * FROM cdiscount_pref where extraction_date like '%{}%'".format(time.strftime("%Y-%m-%d")))
# pref_rows = server_cursor.fetchall()
# df = pd.DataFrame(pref_rows)
# df.to_excel("pdp_output/{}/{}_pref_{}.xlsx".format(date,retailer,date),index=False)

# server_cursor.execute("SELECT * FROM pcworld_pref where extraction_date = '{}'".format(time.strftime("%Y-%m-%d")))
# pref_rows = server_cursor.fetchall()
# df = pd.DataFrame(pref_rows)
# df.to_excel("pdp_output/{}/{}_pref_{}.xlsx".format(date,'pcworld',date),index=False)

cursor.execute("SELECT * FROM mediamarkt_pdp_crawl  where date like '%2021-07-21%'")
rows = cursor.fetchall()
df = pd.DataFrame(rows)
df.to_excel("mediamarkt_pdp_crawl_{}.xlsx".format(date),index=False)


# cursor.execute("select * from cdiscount_pdp_crawl_new")
# rows = cursor.fetchall()
# df = pd.DataFrame(rows)
# df.to_excel("pdp_output/{}/{}_pdp_crawl_{}.xlsx".format(date,retailer,date),index=False)
