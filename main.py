import crawler

c = crawler.Crawler('https://www.crawler-test.com/')
index, graph = c.crawl_web()
print("initializing crawler")
ranks = crawler.compute_ranks(graph)
keyword = input("Input the keyword: ")

print(crawler.lucky_search(index, ranks, keyword))
print(crawler.all_search(index, ranks, keyword))