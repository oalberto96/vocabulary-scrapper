import scrapy
from scrapy.crawler import CrawlerProcess
import sys


class DWSpider(scrapy.Spider):
    name = 'DW'

    def __init__(self, url='', *args, **kwargs):
        super(DWSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    # start_urls = self.start_urls = [kwargs.get('start_url')]
    # [
    # 'file:///home/glassy/Documents/Vocabulary%20_%20Ich%20hei%C3%9Fe%20Emma%20_%20DW%20Learn%20German.html']

    def parse(self, response):
        title = response.css('h1::text').get()
        vocabulary = []
        for row in response.xpath('//div[contains(@class, "row") and contains(@class, "vocabulary")]'):
            concept = {}
            concept['german'] = row.css(
                '.audio-wortschatz-link > span > strong::text').get()
            concept['audio'] = row.css(
                '.audio-wortschatz-link').css('source::attr(src)').get()
            concept['english'] = row.css(
                '.col-sm-4.col-lg-3.vocabulary-entry > .richtext-content-container').css('p::text').get()
            vocabulary.append(concept)
        data = {}
        data["title"] = title
        data["data"] = vocabulary
        yield data


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(DWSpider, sys.argv[1])
    process.start()  # the script will block here until the crawling is finished
