from scrapy.contrib.loader import XPathItemLoader
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
import os
import subprocess
import re
import csv
import urllib2
import sys

if (len(sys.argv) >= 2):
    #if used from command line
    DOMAIN = sys.argv[1]
    NAME = sys.argv[2]
    START_URLS = sys.argv[3]
else:
    #if not used from command line set the domain to scrape here:
    DOMAIN ="www.firstsearchblue.com"
    #set the name of the output file here:
    NAME = "FIRSTSEARCHBLUE"
    #set the starting URL for the scrape here (try to find a page with as many links a s possible):
    START_URLS = 'http://firstsearchblue.com/'
    
URL = 'http://%s' % DOMAIN
url_list =[]
url_dict = {}
url_dodge_japan = []
url_japan_dict = {}

the_dir = os.path.dirname(__file__)

# function to find the tag and query parameters from the http traffic output string   
def get_http_dict(theFile):
    #Split the output into an array
    stripFile = theFile.strip()
    
    #%#Set pattern for the analytics request
    pattern = re.compile(r"www\.google\-analytics\.com\/\_\_utm\.gif\?")
    
    #%#Set patern for any parameters we want to find (e.g. pagename)
    title_pattern = re.findall(r"&utmdt\=([^\,]*?)&",stripFile)
    
    #Un-encode any parameters for uman readers!
    if len(title_pattern) >0:
        unencoded_title = urllib2.unquote(title_pattern[0])
    else:
        unencoded_title = "no title"
    mid_result = pattern.search(stripFile)
    if mid_result != None:
        result = True
    else:
        result = False
    print unencoded_title
    full_result = [result,unencoded_title]
    return full_result

#Set path variable for phantom - if running in Windows, ensure that the path to 
# Phantomjs and Casperjs are defined in the system PATH variable
PHANTOM = 'phantomjs'
SCRIPT = os.path.join(the_dir, 'phantom_sniff.js')


def runcmd(the_url):
    params = [PHANTOM, SCRIPT,the_url]
    phantomproc = subprocess.Popen(params,shell=False,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    output = phantomproc.communicate()[0]
    exit_code=phantomproc.wait()    
    return exit_code, output

def get_http(UrlPass):
    #Start new phantom process
    print UrlPass+" is being retrieved."
    http_traffic = runcmd(UrlPass)
    list_output = get_http_dict(http_traffic[1])
    print UrlPass+"Request: "+str(list_output[0])
    return list_output

class MySpider(BaseSpider):
    name = DOMAIN
    allowed_domains = [DOMAIN]
    start_urls = [START_URLS]

    def parse(self, response):
        new_url = response.url
        if new_url.startswith(URL):
            url_list.append(new_url)
            
        split_url = new_url.split('/')
        
        #Start the spider!
        try:
            hxs = HtmlXPathSelector(response)
            for url in hxs.select('//a/@href').extract():
                #General link Rules
                if (not url.startswith('http://')) and (not url.startswith('/')) and (not url.startswith('https://')):
                    url= URL +"/"+ url
                if url.startswith('..'):
                    url = URL + url[2:]
                if (not url.startswith('http://')) and (not url.startswith('https://')):
                    url= URL + url
                print url
                if url.startswith("#"):
                    continue
                if url.endswith('.pdf') or url.endswith('.jpg') or url.endswith('.JPG') or url.endswith('.flv') or url.endswith('.doc') or ('javascript' in url) or ('mailto' in url) or ('/feed' in url) or ('/doc/' in url):
                    continue
                if url not in url_list:
                    req =Request(url, callback=self.parse)
                    yield req
        except:
            pass

def main():
    """Setups item signal and run the spider"""
    # set up signal to catch items scraped
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher
    
    
    def catch_item(sender, item, **kwargs):
        print "Got:", item

    # shut off log
    from scrapy.conf import settings
    settings.overrides['LOG_ENABLED'] = False

    # set up crawler
    from scrapy.crawler import CrawlerProcess

    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    crawler.crawl(MySpider())

    # start engine scrapy/twisted
    print "STARTING ENGINE"
    crawler.start()
    print "ENGINE STOPPED"
    

if __name__ == '__main__':
    
    #Run the spider to get all the URLS
    main()
    print url_list
    
    #run phantomjs processes and fill a dictionary with pagetagged[True|False] and pagename[string
    # from the list of urlscreated by main()
    for urlentry in url_list:    
            url_dict[urlentry] = get_http(urlentry)    
    
    print url_dict
    
    #Output to CSV
    csvfile = open(NAME+"-report.csv", 'wt')
    try:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'Tagged?','Title'])
        for key in url_dict:
            writer.writerow([key, url_dict[key][0],url_dict[key][1]])
    finally:
        csvfile.close()