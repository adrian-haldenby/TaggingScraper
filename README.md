Analytics Tag Checking Scraper
========================================
Adrian Haldenby
adouglas@sapient.com


OVERVIEW
--------

This is a two part web scraping script mostly used for checking tagging across many properties,
the first section collects all the links on a website
via crawling the sites with Scrapy or CasperJS (if there are alot of javaqscript links on 
the site). This list of URLS is then passed one by one to Phantom JS to read the HTTP traffic which
is then passed back to python to see if the request for an analytics pixel happens and records the
value of given query parameters.


USAGE
-----

First ensure all dependancies are installed and that phantomjs and casperjs\batchbin directories have 
been added to the system PATH variable.

**Verifying Tagging on Single Sites**

For scraping a single site use the ScrapeMod.py script from the command line. It takes three arguements - the first being the url of the website (without http:// prepended), the name of the output file, and finally the url (including http://) of where you'd like to begin the scraper. 
Begining the scraper on a page with lots of deep links such as an the html sitemap, leads to the fastest scrape

    $ python ScrapeMod.py 'firstsearchblue.com' "First Search Scrape" "http://firstsearchblue.com"

This will output a csv file of each of the URLS on the given site, if its tagged or not, and the page title. By default it looks for Google analytics tags
but it can be used for any analtics package that makes a standerdized off domain request - you just have to change the regular expression in the get_http_dict function.

If you're crawling sites with alot of javascript links, use the just_casper.py file to gather the site links with the headless browser. This has a far higher run time
than the ScrapeMod script so use it only when there are a TON of stupid stupid JS links. It takes two arguements; the url (with http://) of the site you wish to scrape
and the name of the output CSV

    $ python just_casper.py 'http://firstsearchblue.com' 'First Search Scrape' 

**Verifying Tagging on Groups of Sites**

For verifying tags on groups of sites, use the ScrapeAuto.py file. Add sites to the crawl dictionaries according to the template provided and run it with the name of the crawl dictionary as the only arguement.
It comes with 2 sets of crawl dictionaries, SET1 and SET2:

    $ python ScrapeAuto SET1

DEPENDENCIES
------------

**Python Packages**

*Scrapy http://scrapy.org/
*Beautiful Soup version <4 http://www.crummy.com/software/BeautifulSoup/

Installation (on windows):
* Make sure python 2.7 is installed on the machine
* add the C:\python27\Scripts and C:\python27 folders to the system path by adding those directories to the PATH environment variable from the Control Panel.
* Download Easy install version setuptools-0.6c11.win32-py2.7.exe from http://pypi.python.org/pypi/setuptools#downloads and install it
* goto http://pypi.python.org/pypi/pyOpenSSL/0.13, download the windows pyOpenSSL installer and run it
* Install lxml (libxml) by going to  http://pypi.python.org/pypi/lxml/ getting libxml2-python-2.7.7.win32-py2.7.exe and running it.
* To install scrapy open cmd.exe and enter “easy_install scrapy” without the quotations
* To install Beautiful Soup enter "easy_install beautifulsoup" without the quotations
* Done!


**Headless Browser**

PhantomJS http://casperjs.org/
CasperJS http://phantomjs.org

Installation:
Download them from their respective URLs and add the phantomjs and casperjs\batchbin folders to
the system PATH variable.

