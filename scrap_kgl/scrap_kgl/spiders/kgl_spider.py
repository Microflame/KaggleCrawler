import sys
import scrapy

class CompetitionScraper(scrapy.Spider):
    name = "competitions"

    def start_requests(self):
        for url in sys.stdin:
            url = 'https://kaggle.com' + url.strip()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'url': response.url,
            'body': response.text
        }

        self.log('Scraped ' + response.url)


kernel_tmpl =  'https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone&pageSize=100&after=0&competitionId=%s'
discussion_tmpl = 'https://www.kaggle.com/forums/%s/topics.json?sortBy=hot&group=all&page=%d&pageSize=20&category=all'

class KernelScraper(scrapy.Spider):
    name = "kernels"

    def start_requests(self):
        for url, competitionId, discussionId in map(lambda l: l.split(), sys.stdin):
            if url == 'Url':
                continue # skip header
            url = kernel_tmpl % competitionId.strip()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'competitionId': int(response.url.split('=')[-1]),
            'json': response.text
        }

        self.log('Scraped ' + response.url)

class DiscussionScraper(scrapy.Spider):
    name = "discussions"

    def start_requests(self):
        for url, competitionId, discussionId in map(lambda l: l.split(), sys.stdin):
            if url == 'Url':
                continue # skip header
            if discussionId == '-1':
                continue
            for page in range(1, 4):
                url = discussion_tmpl % (discussionId.strip(), page)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'discussionId': int(response.url.split('/')[4]),
            'page': int(response.url.split('&')[3].split('=')[-1]),
            'json': response.text
        }

        self.log('Scraped ' + response.url)
