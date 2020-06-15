import scrapy

class IdnesSpider(scrapy.Spider):
    name = "idnes"
    allowed_domains = ['idnes.cz']
    start_urls = [
        'https://www.idnes.cz/zpravy/archiv/1']

    count = 0

    def parse(self, response):
        articles = response.css('.art > a.art-link')
        yield from response.follow_all(articles, self.parse_article)

        next_page = response.css('#list-art-count a.ico-right')
        yield from response.follow_all(next_page, self.parse)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        if self.count >= self.settings['CLOSESPIDER_ITEMCOUNT'] or response.status != 200:
            return
        self.count += 1

        yield {
            "link": response.url,
            "header": extract_with_css('h1::text'),
            "category": extract_with_css('.portal-g2a a::text'),
            "author": extract_with_css('.name::text'),
            "published_at": extract_with_css('.time-date::text'),
            "opener": extract_with_css('.opener::text'),
            "paragraphs": list(map(lambda a: a.strip(), response.css('#art-text p::text').getall())),
        }