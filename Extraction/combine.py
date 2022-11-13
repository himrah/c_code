import pandas as pd
import numpy as np
import sys
import glob
import time
import os



def BE_Clean(file_name,df):
	if file_name in ["Coolblue_BE_solr_export.xlsx","Mediamarkt_BE_solr_export.xlsx"]:
		df["discount_price"] = df["discount_price"].str.replace(",-","").str.replace(".","").str.replace(",",".")
	return df


def CH_Clean(file_name,df):
	if file_name in["Brack_CH_solr_export.xlsx","Microspot_CH_solr_export.xlsx"]:
		# print(file_name)
		df["price"] = np.where(df["price"].isna(),np.nan,df["price"].astype(str).str.replace("""'""",""))
		df["discount_price"] = np.where(df["discount_price"].isna(),np.nan,df["discount_price"].astype(str).str.replace("""'""","").str.replace("CHF ","").str.replace(".– –",""))
	return df


def DK_Clean(file_name,df):
	if file_name in ["Fcomputer_DK_solr_export.xlsx","Wupti_DK_solr_export.xlsx"]:
		df["price"] = np.where(df["price"].isna(),np.nan,df["price"].astype(str).str.replace("DKK","").str.replace(",-","").str.replace(".","").str.replace(",","."))
		df["discount_price"] = np.where(df["discount_price"].isna(),np.nan,df["discount_price"].astype(str).str.replace("DKK","").str.replace(",-","").str.replace(".","").str.replace(",","."))
	return df

def get_files(country,start_date,end_date):

	start = int(start_date.split("-")[-1])
	end = int(end_date.split("-")[-1])
	
	for xls in glob.glob(country+"/Output/"+start_date+"/*.xlsx"):
		file_name = xls.split("/")[-1]
		all_data = pd.DataFrame()
		for i in range(start,end+1):
			date  = start_date.split("-")[-3] +"-"+ start_date.split("-")[-2]+"-"+ str(i).zfill(2)
			file = country+"/Output/"+date+"/"+file_name.split("/")[-1]
			print(file)
			df = pd.read_excel(file)
			if(file.find("Lenovo_") == -1):
				try:
					df["Date"] = df["Date"].str.split("T").str[0]
				except:
					df["Extraction_Date"] = df["Extraction_Date"].str.split("T").str[0]
			if(country == "BE"):
				df = BE_Clean(file_name,df)
			if(country == "CH"):
				df = CH_Clean(file_name,df)
			if(country == "DK"):
				df = DK_Clean(file_name,df)
			all_data = all_data.append(df,ignore_index=True)
		if(os.listdir("output/").count(time.strftime("%Y-%m-%d")) == 0):
			os.mkdir("output/{}/".format(time.strftime("%Y-%m-%d")))
		if(os.listdir("output/{}".format(time.strftime("%Y-%m-%d"))).count(country) == 0):
			os.mkdir("output/{}/{}".format(time.strftime("%Y-%m-%d"),country))
		all_data.to_excel("output/{}/{}/{}_{}_{}.xlsx".format(time.strftime("%Y-%m-%d"),country,file_name,start,end) ,index=False,header=True)
file,country,start_date,end_date = sys.argv
get_files(country,start_date,end_date)