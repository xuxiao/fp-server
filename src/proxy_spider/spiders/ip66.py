# -*- coding: utf-8 -*-
import json
import time
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from proxy_spider import utils
from proxy_spider.items import Proxy
from proxy_spider.spiders import _BaseSpider


class Ip66Spider(_BaseSpider):
    name = 'ip66'
    allowed_domains = ['www.66ip.com']

    rules = (
        Rule(LinkExtractor(allow=(r'/\d+\.html$', )),
             callback='parse',
             follow=True),
    )

    def start_requests(self):
        base = 'http://www.66ip.cn'
        meta = {
            # 'max_retry_times': 10,
            'download_timeout': 20,
        }

        for _page in range(1, 10):
            if self.complete_condition():
                break
            url = urljoin(base, '/%s.html' % _page)
            yield Request(url, meta=meta, dont_filter=True)

    def parse(self, response):
        for tr in response.xpath('//div[@id="main"]//table/tr')[1:]:
            ex = tr.xpath('./td/text()').extract()
            ip = ex[0]
            port = ex[1]

            if ip and port:
                for scheme in ('http', 'https'):
                    yield self.build_check_recipient(ip, port, scheme)
