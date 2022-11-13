
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

mail_sender = "compete.alert@course5i.com"
mail_protocol = ["smtp.office365.com",587]
mail_credentials = ["compete.alert@course5i.com", "tkcdbgjxtylfkrzj"]

# to_list = ["sunil.dhasmana@course5i.com","rahul.kumar@course5i.com","devender@course5i.com"]
# all_recipients = ["sunil.dhasmana@course5i.com","rahul.kumar@course5i.com","devender@course5i.com"]

to_list = ["rahul.kumar@course5i.com","devender@course5i.com"]
all_recipients = ["rahul.kumar@course5i.com","devender@course5i.com"]

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
        width: 100%;
        
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
    html = open("table1.html","r").read()
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
    smtpObj.sendmail(mail_sender, receiver, message)
    print("Sent Mail Successfully..")
create_msg()

def CreateTable():
    date = time.strftime("%Y-%m-%d")
    countries = ["BE","CH","DK","FI","NO","SE","DE","IT","UK","FR","ES","NL"]
    data = []
    for country in countries:
        d = country + "/output/"+date
        files = glob.glob(f"{d}/*.xlsx")
        for file in files:
            df = pd.read_excel(file)
            count = len(df)
            retailer = file.split("/")[-1].split("_")[0]
            print(f"{country} : {retailer} : {count}")
            data.append({
                "Country":country,
                "Retailer":retailer,
                "Count":count,
                "Date":date
            })
    df = pd.DataFrame(data)
    # df.to_excel(f"counting_{date}.xlsx",index=False)
    return df

# def runnder():
#     os.system()


# runner()
df = CreateTable()
create_msg(df)

