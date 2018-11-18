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

