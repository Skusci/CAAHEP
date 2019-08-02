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
        ProgramId = r.get('id')[7:];
        City = str(r.find('h5', attrs={'class': 'cbp-nttrigger cbp-first col-md-2 col-sm-3 col-xs-3'}).contents[0].string)
        State = str(r.find('span', attrs={'class': 'StateTitle'}).string)
        Institution = str(r.find('h3', attrs={'class' : 'cbp-nttrigger col-md-4 col-sm-3 col-xs-3'}).string)
        Profession = str(r.find_all('h3', attrs={'class' : 'cbp-nttrigger col-md-3 col-sm-3 col-xs-3'})[0].string)
        Concentration = str(r.find_all('h3', attrs={'class' : 'cbp-nttrigger col-md-3 col-sm-3 col-xs-3'})[1].string)
        
        Address = r.find('div', attrs={'class' : 'program-address col-md-6 col-sm-6 col-xs-6'}).find('p')
        Address1 =  str(Address.contents[0].string)
        Address2 =  str(Address.contents[2].string)
        Address3 =  str(Address.contents[4].string)
        Address4 =  str(Address.contents[6].string)

        
        ProgInfo = r.find('div', attrs={'class' : 'program-info col-md-6 col-sm-6 col-xs-6'}).find('p')
        
        ProgStatus = str(ProgInfo.contents[1].string)
        ProgAccredDate = str(ProgInfo.contents[1].string)
        ProgDegrees = str(ProgInfo.contents[1].string)
        ProgDirector = str(ProgInfo.contents[1].string)
        ProgPhone = str(ProgInfo.find_all('a')[0].string)
        ProgEmail = str(ProgInfo.find_all('a')[1].string)
        ProgAward = str(ProgInfo.find_all('a')[2].get('href'))
        
        
        Website = str(r.find('h4', attrs={'class' : 'website'}).contents[0].string)
        
        program = {
            'ProgramId' : ProgramId,
            'City': City,
            'State': State,
            'Institution Name': Institution,
            'Profession': Profession,
            'Concentration': Concentration,
            'Address Line 1': Address1,
            'Address Line 2': Address2,
            'Address Line 3': Address3,
            'Address Line 4': Address4,
            'Program Status': ProgStatus,
            'Accredation Date': ProgAccredDate,
            'Degrees' : ProgDegrees,
            'Director': ProgDirector,
            'Phone' :ProgPhone,
            'E-Mail' : ProgEmail,
            'Award Link' : ProgAward,
            'Website': Website,
        }
        
        programs.append(program)
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

scraperwiki.sqlite.save(['ProgramId'], results)
