
import glob
import pandas as pd
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import collections
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import schedule
from datetime import datetime, timedelta
import jinja2



mail_sender = "compete.alert@course5i.com"
mail_protocol = ["smtp.office365.com",587]
mail_credentials = ["compete.alert@course5i.com", "tkcdbgjxtylfkrzj"]

# to_list = ["sunil.dhasmana@course5i.com","rahul.kumar@course5i.com","devender@course5i.com"]
# all_recipients = ["sunil.dhasmana@course5i.com","rahul.kumar@course5i.com","devender@course5i.com"]

# to_list = ["rahul.kumar@course5i.com","devender@course5i.com","sunil.dhasmana@course5i.com","sunil1.kumar@course5i.com"]
# all_recipients = ["rahul.kumar@course5i.com","devender@course5i.com","sunil.dhasmana@course5i.com","sunil1.kumar@course5i.com"]

to_list = ["rahul.kumar@course5i.com"]
all_recipients = ["rahul.kumar@course5i.com"]
mail_subject = "EMEA Consumer count alert"


style = """
<br>
<span>
    Hi Team
</span>
<div>
    Please find the table below for <b>EMEA consumer</b> count
</div><br>


<style>
    *{
        font-size: 13px;
        font-family: Arial, Helvetica, sans-serif;
    }
    table{
        font-family: Arial, Helvetica, sans-serif;
        
    }
    tr{
        color: unset;
    }
    td{
        font-size: 13px;
        color: unset;
        padding: 10px;
        border-top: 1px solid gray;
    }
    th{
        font-size: 13px;
        text-align: left;
        padding: 10px;
        color: unset;
    }
    table tbody tr:nth-child(1n){
        background-color: #CCC;    
    }

  table tbody tr:nth-child(2n){
    background-color: white;    
  }    
</style>
"""

signature = """
<br>
<div>
    Regards<br>
    Compete Team
</div>
"""



def create_msg(df):
    #html = open("table1.html","r").read()
    html = df.to_html(index=False)
    html = html.replace('<table border="1" class="dataframe">','<table class="dataframe" cellspacing="0",cellpadding="0">')
    html = style + html + signature
    msg = MIMEMultipart()
    part = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    msg.attach(part)
    # return message
    msg['Subject'] = mail_subject
    msg['To'] = ",".join(to_list)
    msg['From'] = "Compete Alert"
    message = msg.as_string()
    smtpObj = smtplib.SMTP(mail_protocol[0],mail_protocol[1])
    smtpObj.starttls()
    smtpObj.login(mail_credentials[0],mail_credentials[1])
    receiver = ",".join(to_list)
    smtpObj.sendmail(mail_sender, all_recipients, message)
    print("Sent Mail Successfully..")
#create_msg()

# date = datetime.strftime(datetime.now(), '%Y-%m-%d')
# datey = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')


# def Formating(data):
#     headers = list(data[0].keys())[:-1]
#     datey = headers[-1]
#     date = headers[-2]
#     templateLoader = jinja2.FileSystemLoader(searchpath="./")
#     templateEnv = jinja2.Environment(loader=templateLoader)
#     template = templateEnv.get_template("sxs.html")
#     c = template.render(headers = headers,date = date,datey = datey,data = data)



def CreateTable():
    # date = time.strftime("%Y-%m-%d")
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    datey = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    countries = ["BE","CH"]
    data = []
    for country in countries:
        d = country + "/output/"+date
        files = glob.glob(f"{d}/*.xlsx")
        for file in files:
            df = pd.read_excel(file)
            today_count = len(df)
            df1 = pd.read_excel(file.replace(date,datey))
            y_count = len(df1)
            # retailer = file.split("/")[-1].split("_")[0].split("\\")[1]
            retailer = file.split("/")[-1].split("_")[0]
            print(f"{country} : {retailer} : {today_count} : {y_count}")
            data.append({
                "Country":country,
                "Retailer":retailer,
                f"{date}":today_count,
                f"{datey}":y_count,
                "Changes":today_count - y_count
                # "Date":date
            })
    df = pd.DataFrame(data)
    return df

def runner():
    os.system("python solr_cmn_v4.1.py DE")
    os.system("python solr_cmn_v4.1.py BE")
    os.system("python solr_cmn_v4.1.py CH")
    os.system("python solr_cmn_v4.1.py DK")
    os.system("python solr_cmn_v4.1.py ES")
    os.system("python solr_cmn_v4.1.py FI")
    os.system("python solr_cmn_v4.1.py FR")
    os.system("python solr_cmn_v4.1.py IT")
    os.system("python solr_cmn_v4.1.py NL")
    os.system("python solr_cmn_v4.1.py NO")
    os.system("python solr_cmn_v4.1.py SE")
    os.system("python solr_cmn_v4.py UK")



def job():
    # runner()
    df = CreateTable()
    create_msg(df)

job()
# schedule.every().day.at("11:30").do(job)
# while True:
#     schedule.run_pending()
#     time.sleep(1)