#!/usr/bin/env python3

import sys

from Parser.spiders.idnes_parser import IdnesArticleSpider, IdnesCommentsParser
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor

if __name__ == "__main__":
    settings = get_project_settings()
    configure_logging()
    runner = CrawlerRunner(settings=settings)

    try:
        number_of_pages = int(sys.argv[1])
    except IndexError or ValueError:
        number_of_pages = 10
    settings.update({'CLOSESPIDER_ITEMCOUNT': number_of_pages})

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(IdnesArticleSpider)
        yield runner.crawl(IdnesCommentsParser)
        reactor.stop()

    crawl()
    reactor.run()
