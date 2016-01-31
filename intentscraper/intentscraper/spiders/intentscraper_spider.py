import re
import sys
import json
import scrapy

from intentscraper.items import IntentscraperItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import BaseSpider, Spider
from urlparse import urljoin
from intentscraper.items import IntentscraperItem


class IntentSpider(CrawlSpider):
    name = "intentscraper"
    # allowed_domains = ["phpmongotweet-portalresearch.rhcloud.com"]
    # rules = (Rule(SgmlLinkExtractor(), callback='parse_items', follow=True),)
    # start_urls = ['http://phpmongotweet-portalresearch.rhcloud.com/']

    def __init__(self, *args, **kwargs):
        super(IntentSpider, self).__init__(*args, **kwargs)
        urls = kwargs.get('urls')
        self.domain = kwargs.get('domain')
        self.start_urls = [urls]
        self.allowed_domains = [self.domain]
        self.crawledLinks = []


    def parse(self, response):
        hxs = scrapy.Selector(response)
        links = hxs.xpath("//a/@href").extract()
        p = IntentscraperItem()
        try:
            p['domain'] = self.domain
            crawledUrl = response.url
            p['url'] = crawledUrl
            rawData = response.body
            scriptLinks = response.xpath('//script/@src').extract()
            for n, i in enumerate(scriptLinks):
                scriptLinks[n] = urljoin(self.start_urls[0], i)
            styleLinks = response.xpath('//link[@rel="stylesheet"]/@href').extract()
            for n, i in enumerate(styleLinks):
                styleLinks[n] = urljoin(self.start_urls[0], i)
            data = {
                'raw':rawData,
                'scripts':scriptLinks,
                'styles':styleLinks,
                'analysis': 'to be done later',
                'tags':'to be done later'}
            data = json.dumps(data)
            p['jsondata'] = data
            p.save()
        except:
            pass
        for n, i in enumerate(links):
            links[n] = urljoin(self.start_urls[0], i)

        linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        for link in links:
            # If it is a proper link and is not checked yet, yield it to the Spider
            if linkPattern.match(link) and not link in self.crawledLinks:
                self.crawledLinks.append(link)
                yield scrapy.Request(link, callback = self.parse)

    def parse_category(self, response):
        filename = response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)


