from bs4 import BeautifulSoup
import urllib2
import urlparse
import random

base_url = "http://en.wikipedia.org/wiki/"
base_wiki_page = "List_of_Python_software"
goal_term = "Confiscation"
goal_url = base_url + goal_term

def get_page(url):
    """
        Grabs the current page file
    """
    request = urllib2.Request(url, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    page_file = urllib2.urlopen(request)
    return page_file

def check_wiki(goal_page, visted_sites):
    """
        Checks if page has already been visited.
    """
    if goal_page in visted_sites:
        return True
    else:
        return False

def get_next_link(page_links, base_url, base_wiki_page):
    """
        Gets the next link
    """
    temp_list = []
    for link in page_links:
        if link.startswith('/wiki/'):
            next_page = link.strip('/wiki/').split(':')[0]
            next_link = base_url + next_page
            temp_list.append(next_link)
        else:
            pass
    if check_wiki(goal_url, temp_list):
        next_link = goal_url
    else:
        if temp_list:
            if len(temp_list) >= 1:
                random_index = random.randint(0, len(temp_list)-1)
            else:
                random_index = 0
            next_link = temp_list[random_index]
            return next_link
        else:
            return base_url + base_wiki_page

def gather_onpage_wikis(soup, goal_term, visted_sites):
    """
        Grabs 'a' - hrefs from the wiki page and chucks them into 
    """
    on_page_links = {}
    for i in soup.findAll('a', href=True):
        on_page_links[i.text] = i['href']
        if goal_term in on_page_links.keys():
            on_page_links = {i.text : i['href']}
    return on_page_links


current_page = base_url + base_wiki_page
visted_sites = {}
count = 1
print "IT BEGINS:\n*********************************************\n" 

while True:
    try:
        soup = BeautifulSoup(get_page(current_page).read())
    except urllib2.HTTPError:
        pass
    else:
        print "Attempt #%r - Trying:\t%r" % (count, current_page)
        title = current_page.split("http://en.wikipedia.org/wiki/")[1]
        visted_sites[title] = current_page
        count += 1
        temp_link_dict = gather_onpage_wikis(soup, goal_term, visted_sites)
        next_page = get_next_link(temp_link_dict.values(), base_url, base_wiki_page)
        if next_page == goal_url:
            print "Found it! %r took %r clicks (URL: %r)" % (title, count, next_page)
        else:
            current_page = next_page
