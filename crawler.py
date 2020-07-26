import operator

def get_page(url):
    try:
        import requests
        return requests.get(url).text
    except:
        return ""


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
           
            #Insert Code Here
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len (graph[node]))
                    
            newranks[page] = newrank
        ranks = newranks
    return ranks


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


def add_page_to_index(index,url,content):
    words = content.split()
    for keyword in words:
        add_to_index(index,keyword,url)


def all_search(index, ranks, keyword):
    print("all search")
    all_search_result = lookup(index, keyword)    
    if len(all_search_result) == 0: return None

    page_rank_dic = {}
    for item in all_search_result:
        page_rank_dic[item] = ranks[item]

    sorted_pages = sorted(page_rank_dic.items(), key = operator.itemgetter(1), reverse=True)
    
    return  [item[0] for item in sorted_pages] 


def lucky_search(index, ranks, keyword):
    pages=lookup(index,keyword)
    if not pages:
        return None
    best_page=pages[0]
    for candidate in pages:
        if ranks[candidate]>ranks[best_page]:
            best_page=candidate
    return best_page


def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return index

class Crawler:
    
    def __init__(self, seed):
        self.seed = seed

    def crawl_web(self):
        print("crawling web")
        tocrawl = [self.seed]
        crawled = []
        index = {}
        graph = {}
        while tocrawl:
            page = tocrawl.pop()
            if page not in crawled:
                content = get_page(page)
                add_page_to_index(index, page, content)
                outlinks = get_all_links(content)
                
                graph[page] = outlinks
                union(tocrawl, outlinks)
                crawled.append(page)
                
        return index, graph  