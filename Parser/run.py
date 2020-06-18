#!/usr/bin/env python3

import sys

from Parser.spiders.idnes_parser import IdnesArticleSpider, IdnesCommentsParser
from scrapy.crawler import CrawlerRunner
# from scrapy.utils import defer, reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

if __name__ == "__main__":
    settings = get_project_settings()
    configure_logging()
    runner = CrawlerRunner(settings=settings)
    settings.update({'CLOSESPIDER_ITEMCOUNT': int(sys.argv[1])})

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(IdnesArticleSpider)
        yield runner.crawl(IdnesCommentsParser)
        reactor.stop()


    crawl()
    reactor.run()

'''
def refresh(number:int = 10):
    settings = get_project_settings()

    configure_logging()
    runner = CrawlerRunner(settings=settings)
    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(IdnesArticleSpider)
        yield runner.crawl(IdnesCommentsParser)
        reactor.stop()
    settings.update({'CLOSESPIDER_ITEMCOUNT': number})
    crawl()
    reactor.run()
    '''