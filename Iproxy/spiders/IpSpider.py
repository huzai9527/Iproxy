import scrapy
import Iproxy.items


class IpSpider(scrapy.Spider):
    name = 'IpSpider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    def parse(self, response):
        item = Iproxy.items.IproxyItem()
        item['ip'] = response.css('tr td:nth-child(2)::text').extract()
        item['port'] = response.css('tr td:nth-child(3)::text').extract()
        item['type'] = response.css('tr td:nth-child(6) ::text').extract()
        yield item

