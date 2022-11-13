import schedule
import os
print(os.getcwd())
def job():
    os.system("python pcworld_crawl.py")
    os.system("python cyberport_crawl.py")
    
# run the function job() every 2 seconds 
# job()
# schedule.every(79200).seconds.do(job)
schedule.every().day.at("05:30").do(job)


while True:  
    schedule.run_pending()