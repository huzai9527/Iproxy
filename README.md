# 用scrapy爬取可用的代理
## 分析免费代理网站的结构
- 我爬取了三个字段：**IP**、**port**、**type**
![TIM图片20181118171534.jpg](https://i.loli.net/2018/11/18/5bf12dc61a906.jpg)
## 分析要爬取的数据，编写items.py
- 因此在items.py中，建立相应的字段
```bash
import scrapy
class IproxyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    type = scrapy.Field()
    port = scrapy.Field()
```
## 爬取所有的免费ip
- 在spider目录下，创建IpSpider.py
```bash
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
```
## 检测是否可用，如果可用则存入数据库
- 因为是免费的ip，所以我们有必要检测一下他是否可用，对于可用的就存入数据库，反之则丢弃
- 检测处理数据在pipeline.py中编写
- 检测原理，通过代理访问百度，如果能够访问，则说明可用
```bash
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import requests

class IproxyPipeline(object):
    def process_item(self, item, spider):
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        db = pymysql.connect("localhost", "root", "168168", "spider")
        cursor = db.cursor()
        for i in range(1, len(item['ip'])):
            ip = item['ip'][i] + ':' + item['port'][i]
            try:
                if self.proxyIpCheck(ip) is False:
                    print('此ip：'+ip+"不能用")
                    continue
                else:
                    print('此ip：'+ip+'可用，存入数据库！')
                    sql = 'insert into proxyIp value ("%s")' % (ip)
                    cursor.execute(sql)
                    db.commit()
            except:
                db.rollback()
        db.close()
        return item

    def proxyIpCheck(self, ip):
        proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
        try:
            r = requests.get('https://www.baidu.com/', proxies=proxies, timeout=1)
            if (r.status_code == 200):
                return True
            else:
                return False
        except:
            return False


```
## 运行情况
- 可以看出还是有好多ip不能用的
![TIM图片20181118172712.png](https://i.loli.net/2018/11/18/5bf1308222b42.png)
- 可用的存在数据库

![TIM图片20181118172841.jpg](https://i.loli.net/2018/11/18/5bf130d8031b3.jpg)












