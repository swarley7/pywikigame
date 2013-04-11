from bs4 import BeautifulSoup
import urllib2
import urlparse
import random
import sys
import socket

base_wiki_page = 'Python'
goal_term = 'Confiscation'


base_url = "http://en.wikipedia.org/wiki/"
#base_wiki_page = sys.argv[1]
#goal_term = sys.argv[2]
goal_url = base_url + goal_term

def get_page(url):
    """
        Grabs the current page file
    """
    error_count = 0
    request = urllib2.Request(url, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    while True:
        try:
            page_file = urllib2.urlopen(url=request,timeout=1)
        except urllib2.URLError, e:
            if error_count <=5:
                print("There was an error: %r" % e)
                error_count += 1
            else:
                print "Unable to get file %r" % url
                sys.exit(1)
        except socket.timeout, e:
            if error_count <=5:
                print ("There was an error: %r" % e)
                error_count += 1
            else:
                print "Unable to get file %r" % url
                sys.exit(1)
        else:
            return page_file
            break

def check_wiki(goal_page, visited_sites):
    """
        Checks if page has already been visited.
    """
    if goal_page in visited_sites:
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

def gather_onpage_wikis(soup, base_url ,goal_term, visited_sites):
    """
        Grabs 'a' - hrefs from the wiki page and chucks them into 
    """
    on_page_links = {}
    page_content = soup('div', {'id':'bodyContent'})
    for bodyContent in page_content:
        links = bodyContent.findAll('a', href=True)
        for i in links:
            if i.text in visited_sites.keys():
                pass
            else:
                on_page_links[i.text] = i['href']
    if goal_term in on_page_links.keys():
        on_page_links = {goal_term : base_url}
    return on_page_links


current_page = base_url + base_wiki_page
visited_sites = {}
count = 1
print "Start: %r (URL: %r)" % (base_wiki_page, base_url + base_wiki_page)
print "Goal: %r (URL: %r)" % (goal_term, base_url + goal_term)
print "IT BEGINS:\n*********************************************\n" 

while True:
    try:
        soup = BeautifulSoup(get_page(current_page).read())
    except urllib2.HTTPError:
        pass
    else:
        print "Attempt #%r - Trying:\t%r" % (count, current_page)
        title = current_page.split("http://en.wikipedia.org/wiki/")[1]
        visited_sites[title] = current_page
        count += 1
        temp_link_dict = gather_onpage_wikis(soup, base_url, goal_term, visited_sites)
        try:
            next_page = get_next_link(temp_link_dict.values(), base_url, base_wiki_page)
        except ValueError:
            print "Attempt failed"
            pass
        else:
            if next_page == goal_url:
                print "Found it! %r took %r clicks (URL: %r)" % (title, count, next_page)
                break
            else:
                current_page = next_page
