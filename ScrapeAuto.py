import sys
import os
import subprocess
import time
import datetime

if (len(sys.argv) >= 1):
    MARKET = sys.argv[1]
else:
    TOCRAWL = "SET1"
    
now = datetime.datetime.now()
date= "%d %d %d" % (now.month,now.day,now.year)


#Add sites to the crawl dictionaries where the key is the URL, the value is a list of [file name, starting URL]
# if the site has alot of Javascript links, add an extra true to the end of the the value list

Crawl_Set1_dict = {
    'www.firstsearchblu.com':['SING CHRYSLER '+ date,'http://www.chrysler.com.sg/lineup.html'],\
    'www.firstsearchblu.com':['SING CHRYSLER '+ date,'http://www.chrysler.com.sg/lineup.html'],\
    #heavy JS links
    'www.dodge.com.co':['LAT_COLUMBIA DODGE '+ date,'http://www.dodge.com.co/mapa-sitio/',True]              
              }

Crawl_Set2_dict = {
         'www.putlockerapp.com':['Putlocker App! '+ date,'http://www.putlockerapp.com',True]
              }


#don't modify
Crawl_Dict = {}



if __name__ == '__main__':
    
    if TOCRAWL == "SET1":
        Crawl_Dict = Crawl_Set1_dict
    elif TOCRAWL == "SET2":
        Crawl_Dict = Crawl_Set2_dict
    else:
        print "Please select either SET1 or SET2 and run again"
        
    if len(Crawl_Dict) >0:
        for key in Crawl_Dict:
            if len(Crawl_Dict[key]) == 3:
                tempkey = 'http://'+key
                params = ['Python','just_casper.py',tempkey,Crawl_Dict[key][0]]
                subprocess.Popen(params)
                time.sleep(1000)
            else:
                params = ['Python','ScrapeMod.py',key,Crawl_Dict[key][0],Crawl_Dict[key][1]]
                subprocess.Popen(params)
                time.sleep(700)
