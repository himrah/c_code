import schedule
import os
import time
def job():
    # os.chdir("mediamarkt")
    os.system("python3 mediamarkt_selenium_crawler.py")
    # os.chdir("../saturn")
    # os.system("python selenium_crawler_saturn.py ")
    # os.chdir("../cdiscount")	
    # os.system("python c_discount_selenium.py")
    # os.chdir("..")
    
    
# run the function job() every 2 seconds 
#job() 
schedule.every().day.at("03:30").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
# schedule.every(79200).seconds.do(job)

# while True:  
#     schedule.run_pending()