from Crawler.Crawler import Crawler
import Crawler.Consts as consts

def main(crawler):
    crawler.start()

if __name__ == '__main__':
    my_crawler = Crawler(consts.url, consts.email, consts.password)
    main(my_crawler)
