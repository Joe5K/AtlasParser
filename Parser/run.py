from scrapy.crawler import CrawlerProcess, CrawlerRunner
#from scrapy.utils import defer, reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from Parser.spiders.idnes_parser import IdnesArticleSpider, IdnesCommentsParser
from twisted.internet import defer, reactor

settings = get_project_settings()

configure_logging()
settings.update({'CLOSESPIDER_ITEMCOUNT': 10})
runner = CrawlerRunner(settings=settings)

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(IdnesArticleSpider)
    yield runner.crawl(IdnesCommentsParser)
    reactor.stop()

crawl()
reactor.run()