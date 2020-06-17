import scrapy
import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from ..items import IdnesItem, IdnesCommentItem


class IdnesArticleSpider(scrapy.Spider):
    name = "idnes"
    allowed_domains = ['idnes.cz']
    start_urls = [
        'https://www.idnes.cz/zpravy/archiv?datum=&idostrova=idnes']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Parser.pipelines.MongoArticlePipeline': 300,
        }
    }
    count = 0


    def parse(self, response):
        articles = response.css('.art > a.art-link::attr(href)').getall()
        yield from response.follow_all(articles, self.parse_article)
        next_page = response.css('#list-art-count a.ico-right')
        yield from response.follow_all(next_page, self.parse)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        if response.status != 200 or self.count >= self.settings['CLOSESPIDER_ITEMCOUNT']:
            return
        self.count += 1
        item = IdnesItem()
        item["link"] = response.url
        item["header"] = extract_with_css('h1::text')
        item["category"] = extract_with_css('.portal-g2a a::text')
        item["author"] = extract_with_css('.authors span::text')
        item["published_at"] = extract_with_css('.time-date::text')
        item["opener"] = extract_with_css('.opener::text')
        item["paragraphs"] = list(map(lambda a: a.strip(), response.css('#art-text p::text').getall()))
        item['comments'] = []
        yield item


class IdnesCommentsParser(scrapy.Spider):
    name = "idnes_comments"
    allowed_domains = ['idnes.cz']
    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 0,
        'ITEM_PIPELINES': {
            'Parser.pipelines.MongoCommentsPipeline': 300,
        }
    }
    count = 0

    def start_requests(self):
        import pymongo
        client = pymongo.MongoClient(self.settings.get('MONGO_URI'))
        database = self.settings.get('MONGO_DATABASE')
        collection_name = self.settings.get('MONGO_COLLECTION_NAME')
        db = client[database]
        urls = [f'{i["link"]}/diskuse/cas' for i in db[collection_name].find({})]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status != 200:
            return
        comments = response.css('.cell').getall()
        for comment in comments:
            item = IdnesCommentItem()

            item['name'] = ''.join(scrapy.Selector(text=comment).css('.name > a::text').getall())
            item['text'] = ''.join(x.strip() for x in scrapy.Selector(text=comment).css('.cell > .user-text > p::text').getall())
            item['date'] = scrapy.Selector(text=comment).css('.cell >.properties >.date::text').get().strip()
            item['link'] = response.url.split('/diskuse/')[0]

            yield item

        next_page = response.css('#disc-list a.ico-right::attr(href)')
        yield from response.follow_all(next_page, self.parse)
