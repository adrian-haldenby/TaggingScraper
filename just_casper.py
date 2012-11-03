import httplib2
import os
import subprocess
import sys
import re
import csv
import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer


#set scrape begin link and name for naming the csv
if (len(sys.argv) >= 2):
    BEGIN = sys.argv[1]
    NAME = sys.argv[2]
else:
    BEGIN ='http://www.jeep-la.com'
    NAME = "LATAM JEEP 08 27"

#debug variable to limit the number of iterations    
counter = 0

#find the current dir
the_dir = os.path.dirname(__file__)

macro_links = []
http = httplib2.Http()
url_dict = {}
javascript_links_list = []

# define the main  crawler function for getting out list of links from a site
def crawlaround(newlinks):
    to_crawl = []
    
    
    for the_crawl in newlinks:

        
        micro_links= []
        missed_links = []
        
        status, response = http.request(the_crawl)
        # make sure we filer out all the links we dont need
        for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
            #get all the links on the page
            if link.has_key('href') and (not link['href'].endswith('.pdf')) and (not link['href'].endswith('.zip')) and (not link['href'].endswith('.jpg')) and (not link['href'].endswith('.jpeg')) and (not link['href'] == " ") and (not link['href'] == "/")  and (not link['href'] == "") and (not link['href'].endswith('.jpg')) and (link['href'] not in macro_links) and (not link['href'].startswith("#")) and (not link['href'].startswith("mailto")) and (not link['href'] in javascript_links_list) and (not link['href'] == the_crawl):
                micro_links.append(link['href'])
            #get all the javascript links so that they are not traversed more than once
            if link.has_key('href') and (not link['href'].endswith('.pdf')) and (not link['href'].endswith('.zip')) and (not link['href'] == " ") and (not link['href'] == "") and (not link['href'].endswith('.jpg')) and (not link['href'].endswith('.jpeg')) and (not link['href'] == "/")  and link['href'].startswith("javascript") and (link['href'] not in macro_links) and (not link['href'].startswith("#")) and (not link['href'].startswith("mailto")) :
                javascript_links_list.append(link['href'])
        print "Start!"  
        # send the links we found on the page to casper to click, returns a list of destination links
        SCRIPT = 'casper_dscrape.js'
        CASPER = "casperjs.bat"
        STARTLINK = the_crawl
        #Encode the command line arguement (for stupid Wwindows)
        LINKLIST = '@'.join(micro_links)
        LINKLIST = re.sub(";","",LINKLIST)
        LINKLIST = re.sub(",","~",LINKLIST)
        LINKLIST = re.sub("'","^'",LINKLIST)
        
        
        #Begin Casper Process:
        # It clicks the first link from the scraped list, rturns where it ends up,
        # goes back and clicks the next link until the list of crawl links
        # is empty.
        params = [CASPER,SCRIPT,STARTLINK, LINKLIST]
        exitcode = subprocess.Popen(params,shell=False,stdout=subprocess.PIPE)
        output = exitcode.communicate()[0]
        print "output:"
        print output
        if len(output)>0:
            output = output.split(",")
        
        # See if we should keep the URLS:
            for url in output:
                url= url.strip()
                if url in macro_links:
                    print " "
                elif url.startswith(BEGIN):
                    to_crawl.append(url)
                    macro_links.append(url)
        else:
            print "Nothing output"
        
        # Not in use right now --
        if len(missed_links)>0:
            for missed in missed_links:
                if (missed not in to_crawl) and (missed not in macro_links) and missed.startswith(BEGIN):
                    macro_links.append(missed)
                    to_crawl.append(missed)
    
    # If we have more links to crawl, recoursively call crawlaround function on those links
    if (len(to_crawl) >0):
        crawlaround(to_crawl)

        
###### Getting the HTTP Traffic from the list of links generated

#Set path variable for phantom
PHANTOM = 'phantomjs'
SCRIPT = os.path.join(the_dir, 'phantom_sniff.js')

# function to find the tag and query parameters from the http traffic output string        
def get_http_dict(theFile):
    #Split the output into an array
    stripFile = theFile.strip()
    #Set patern
    pattern = re.compile(r"gw\.anametrix")
    title_pattern = re.findall(r"&p\.t\=([^\,]*?)&",stripFile)
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
        
def runcmd(the_url):
    params = [PHANTOM, SCRIPT,the_url]
    phantomproc = subprocess.Popen(params,shell=False,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    output = phantomproc.communicate()[0]
    exit_code=phantomproc.wait()    
    return exit_code, output

def get_http(UrlPass):
    #Start nw phantom process
    print UrlPass+" is being retrieved."
    http_traffic = runcmd(UrlPass)
    list_output = get_http_dict(http_traffic[1])
    print UrlPass+"Request: "+str(list_output[0])
    return list_output


if __name__ == '__main__':
    
    macro_links.append(BEGIN)
    
    #assign new urls
    crawlaround(macro_links)
    url_list = macro_links
    print "Break"
    print url_list
    #run phantomjs processes and fill a dictionary with pagetagged[True|False] and pagename[string]
    for urlentry in url_list:    
            url_dict[urlentry] = get_http(urlentry)
    
    #make csv for reporting
    csvfile = open(NAME+"-report.csv", 'wt')
    try:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'Tagged?','Title'])
        for key in url_dict:
            writer.writerow([key, url_dict[key][0],url_dict[key][1]])
    finally:
        csvfile.close()