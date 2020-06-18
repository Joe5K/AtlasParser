import scrapy

from ..items import IdnesItem, IdnesCommentItem


class IdnesArticleSpider(scrapy.Spider):
    name = "idnes"
    allowed_domains = ['idnes.cz']
    start_urls = [
        'https://www.idnes.cz/zpravy/archiv?datum=&idostrova=idnes']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Parser.pipelines.MongoArticlePipeline': 1,
        }
    }
    count = 0


    def parse(self, response):
        articles = response.css('.art > a.art-link::attr(href)').getall()
        for idx, article in enumerate(articles):
            yield response.follow(article, self.parse_article)
            self.count += 1
            if self.count >= self.settings['CLOSESPIDER_ITEMCOUNT']:
                return

        next_page = response.css('#list-art-count a.ico-right')
        yield from response.follow_all(next_page, self.parse)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip().replace(u'\xa0', u' ')

        if response.status != 200:
            return

        item = IdnesItem()
        item["link"] = response.url
        item["header"] = extract_with_css('h1::text')
        item["category"] = extract_with_css('.portal-g2a a::text')
        item["author"] = extract_with_css('.authors span::text')
        item["date"] = extract_with_css('.time-date::text')
        item["opener"] = extract_with_css('.opener::text')
        item["image"] = extract_with_css('div.relative img::attr(src)')
        item["paragraphs"] = [paragraph.strip().replace(u'\xa0', u' ')
                              for paragraph in response.css('#art-text p::text').getall()]
        item['comments'] = []
        yield item


class IdnesCommentsParser(scrapy.Spider):
    name = "idnes_comments"
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 0,
        'CLOSESPIDER_ITEMCOUNT': 0,
        'ITEM_PIPELINES': {
            'Parser.pipelines.MongoCommentsPipeline': 1,
        }
    }

    def parse(self, response):
        if response.status != 200:
            return
        comments = response.css('.cell').getall()
        for comment in comments:

            item = IdnesCommentItem()
            comment_selector = scrapy.Selector(text=comment)

            item['name'] = ''.join(comment_selector.css('.name > a::text').getall())
            item['text'] = ' '.join(paragraph.strip().replace(u'\xa0', u' ')
                                    for paragraph in comment_selector.css('.cell > .user-text > p::text').getall())
            item['date'] = comment_selector.css('.cell >.properties >.date::text').get().strip()
            item['link'] = response.url.split('/diskuse/')[0]

            yield item

        next_page = response.css('#disc-list a.ico-right::attr(href)')
        yield from response.follow_all(next_page, self.parse)
