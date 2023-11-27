import scrapy
import json 
import requests
from scrapy import Spider
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from crawler.items import HrefItem
import re
import time

type = {
    "Tất cả": 0,
    "Báo cáo": 46,
    "Chỉ thị": 1,
    "Công điện": 26,
    "Điều ước quốc tế": 31,
    "Hiến pháp": 6,
    "Hướng dẫn": 9,
    "Kế hoạch": 45,
    "Lệnh": 34,
    "Luật": 10,
    "Nghị định": 11,
    "Nghị định": 11,
    "Nghị quyết": 13,
    "Pháp lệnh": 14,
    "Quyết định": 17,
    "Sắc lệnh": 18,
    "Thông báo": 21,
    "Thông tư": 23,
    "Thông tư liên tịch": 24,
    "Văn bản hợp nhất": 40,
    "Văn bản khác": 33,
    "Văn bản WTO": 32
}

class hrefSpider(Spider):
    name = "co_bao"
    # start_urls = []

    def start_requests(self):
        file_index = getattr(self, 'file_index', 1)
        num = file_index
        file_path = f"info/info_lack.json"

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            law_type_text = item["Tên loại văn bản"]
            law_type = type[law_type_text]
            law_id_text = item["Số, ký hiệu văn bản"]
            law_id = law_id_text.replace("/", "%2F")
            law_name = item["Tên gọi của văn bản/trích yếu nội dung của văn bản"]
            law_issuance_time = item["Ngày, tháng, năm ban hành văn bản"]
            law_effective_time = item["Thời điểm có hiệu lực"]
            law_note = item["Ghi chú"]

            # print("tên: ", item["Tên loại văn bản"])
            # print("type: ", law_type)
            # print("ký hiệu: ", item["Số, ký hiệu văn bản"])
            # print("type: ", law_id)


            url = f"https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword={law_id}&area=2&type={law_type}&status=0&lan=1&org=0&signer=0&match=False&sort=1&bdate=18/11/1943&edate=17/11/2023"
            yield scrapy.Request(url=url, callback=self.parse, meta={'law_type': law_type_text, 'law_id': law_id_text, 'law_name': law_name, 'law_issuance_time': law_issuance_time, 'law_effective_time': law_effective_time, 'law_note': law_note})
            # break #################################

    def parse(self, response):
        law_type = response.meta.get('law_type')
        law_id = response.meta.get('law_id')
        law_name = response.meta.get('law_name')
        law_issuance_time = response.meta.get('law_issuance_time')
        law_effective_time = response.meta.get('law_effective_time')
        law_note = response.meta.get('law_note')

        content_divs = response.css('div[class^="content-"]')
        # print("con: ", content_divs[0])
        if len(content_divs) > 1:
            print(f"Ê, cái {law_id} có 2 link đấy, cẩn thận")
        if len(content_divs) == 0:
            item = HrefItem()
            item["type"] = law_type
            item["id"] = law_id
            item["name"] = law_name
            # item["issuance_time"] = law_issuance_time
            # item["effective_time"] = law_effective_time
            # item["note"] = law_note
            item["href"] = "None"
            item["title"] = "None"
            yield item
        for div in content_divs:
            a_tag = div.css('a[onClick="Doc_CT(MemberGA)"]')
            item = HrefItem()
            item["type"] = law_type
            item["id"] = law_id
            item["name"] = law_name
            # item["issuance_time"] = law_issuance_time
            # item["effective_time"] = law_effective_time
            # item["note"] = law_note
            item["href"] = a_tag.attrib['href']
            item["title"] = a_tag.xpath('string(.)').get()
            yield item

                
            
        


