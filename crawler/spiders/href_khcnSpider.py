import scrapy
import json 
import requests
from scrapy import Spider
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from crawler.items import HrefItemKHCN
import re
import time


class hrefSpider(Spider):
    name = "co_bao_khcn"
    # start_urls = []
    
    # 340
    def start_requests(self):
        file_index = getattr(self, 'file_index', 1)
        num = int(file_index)
        for i in range((num-1)*20 + 1, num*20 + 1):
            url = f"https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=Khoa+h%E1%BB%8Dc+c%C3%B4ng+ngh%E1%BB%87&area=1&match=True&type=0&status=0&signer=0&edate=17/11/2023&sort=1&lan=1&scan=0&org=0&fields=&page={i}"
            yield scrapy.Request(url=url, callback=self.parse, meta={'i': i})

    def parse(self, response):
        i = response.meta.get('i')

        # Lấy tất cả thẻ <a> có thuộc tính onclick="Doc_CT(MemberGA)"
        a_elements = response.css('a[onclick="Doc_CT(MemberGA)"]')
        
        for a in a_elements:
            item = HrefItemKHCN()
            item["i"] = i
            item["href"] = a.attrib['href']
            item["title"] = a.xpath('string(.)').get()
            yield item

                
            
        


