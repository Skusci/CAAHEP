import scraperwiki    
import re
import mechanize
import datetime
from bs4 import BeautifulSoup

starting_page = 'https://www.caahep.org/Students/Find-a-Program.aspx'


def parse_results(html):
    """
    Returns a list of dictionaries that describe the incidents in the given HTML.
    """
    soup = BeautifulSoup(html, "html5lib")
    
    programlist = soup.find('ul', attrs={'id': 'cbp-ntaccordion'})

    programs = []
    for r in programlist.findAll('li', recursive=False):
        Header1 = r.find('h5', attrs={'class': 'cbp-nttrigger cbp-first col-md-2 col-sm-3 col-xs-3'}).contents[0].split("<")[0]
        Header2 = r.find('span', attrs={'class': 'StateTitle'}).contents[0]
        Header3 = r.find('h3', attrs={'class' : 'cbp-nttrigger col-md-4 col-sm-3 col-xs-3'}).contents[0]
        Header4 = r.findall('h3', attrs={'class' : 'cbp-nttrigger col-md-3 col-sm-3 col-xs-3'})[0].contents[0]
        Header5 = r.findall('h3', attrs={'class' : 'cbp-nttrigger col-md-3 col-sm-3 col-xs-3'})[1].contents[0]
        
        Address = r.find('div', attrs={'class' : 'program-address col-md-6 col-sm-6 col-xs-6'}).contents[0]
        
        ProgInfo = r.find('div', attrs={'class' : 'program-info col-md-6 col-sm-6 col-xs-6'}).contents[0]
        Website = r.find('h4', attrs={'class' : 'website'}).contents[0]
        
        program = {
            'header1': Header1,
            'header2': Header2,
            'header3': Header3,
            'header4': Header4,
            'header5': Header5,
            'address': Address,
            'proginfo': ProgInfo,
            'website': Website,
        }
        
        programs.append(incident)
    return programs


def get_pages():
    """
    Returns the HTML of all pages
    """
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')]
    # agree to the disclaimer
    br.open(starting_page)
    # parse the page count and retrieve pages
    pages = []
    for p in range(1, 4):
        print 'Retrieving page %s' % p
        br.select_form(nr=0)
        br.form.set_all_readonly(False)
        br['__EVENTTARGET'] = "p$lt$WebPartZone6$Content$pageplaceholder$p$lt$WebPartZone2$Search$ProgramList$repItems$pager"
        br['__EVENTARGUMENT'] = str(p)
        # remove the "Search" (type=submit) input from the form, otherwise we get the first page of results over and over
        response = br.submit()
        pages.append(response.read())
    return pages



print 'Retrieving results'
pages = get_pages()
print 'Parsing %s pages of results' % len(pages)
results = []
for page in pages:
    results.extend(parse_results(page))

print 'Found %s results, saving in scraperwiki' % len(results)
scraperwiki.sqlite.save(['date', 'location'], results)
