import scrapy
import json 
import requests
from scrapy import Spider
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from crawler.items import LawItem
import re
import time
import copy


class crawlerSpider(Spider):
    name = "co_bao_dieu"

    
    # def parse_homepage(self, response):
    def start_requests(self):
        # Đường dẫn đến file JSON
        file_index = getattr(self, 'file_index', 1)
        num = file_index
        file_path = f"D:\\py\\Lab\\Basic_Crawlers-master\\Basic_Crawlers-master\\co_bao\\href\\href_lack.json"

        # Đọc file JSON
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)


        # Lặp qua từng phần tử trong danh sách
        for item in data:
            # Lấy giá trị title và href của mỗi phần tử
            type = item["type"]
            id = item["id"]
            title = item["title"]
            href = item["href"]

            if href == "None":
                item = LawItem()
                item["type"] = type
                item["id"] = id
                item["href"] = "None"
                item["title"] = "None"
                item["content"] = "None"
                yield item
                continue

            # href = "https://thuvienphapluat.vn/van-ban/Thuong-mai/Thong-tu-01-2009-TT-BKHCN-danh-muc-san-pham-hang-hoa-kha-nang-gay-mat-an-toan-thuoc-trach-nhiem-quan-ly-Bo-Khoa-hoc-Cong-nghe-86912.aspx"
            # Gửi yêu cầu crawl với User Agent tương ứng
            yield scrapy.Request(url=href, callback=self.parse, meta={'type': type, 'id': id, 'title': title, 'href': href})
            # break



    def parse(self, response):
        # time.sleep(0.5)  # Delay 0.5 giây
        cnt_table_begin = 2
        checkTableHead = False
        cnt_table = 2 # số lượng table để nó dừng
        
        div_selector = response.xpath(f'//div[@id="divContentDoc"]/div[@class="content1"]/div/div')
        # print("len:", len(div_selector[0].extract()))
        # # Đếm số lượng thẻ con trực tiếp của phần tử <div> trong danh sách div_selector
        # num_children = div_selector.xpath('count(*)').extract_first()

        # print("Số thẻ con trong câu truy vấn XPath:", num_children)

        if (not any(div.xpath('./div') for div in div_selector)) or float(div_selector.xpath('count(*)').extract_first()) > 10 :
            # Có dữ liệu, bạn có thể sử dụng div_selector ở đây
            # print("day la:", 1)
            pass
        elif any(div.xpath('./div') for div in div_selector):
            # Nếu không có dữ liệu, thay đổi câu truy vấn
            # print("day la:", 2)
            div_selector = response.xpath('//div[@id="divContentDoc"]/div[@class="content1"]/div/div/div')
        else:
            # print("day la:", 3)
            div_selector = response.xpath(f'//div[@id="divContentDoc"]/div[@class="content1"]/div/div')
        # Lưu danh sách các đối tượng div_selector vào một danh sách
        # Tạo nội dung HTML từ các phần tử con của div_selector
        html_content = ""
        for index, div_content in enumerate(div_selector, start=1):
            div_html = div_content.get()
            html_content += f"{div_html}"

        # Tạo đối tượng BeautifulSoup để lưu vào file HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # child_tags = [tag for tag in soup.children if tag.name]

        # Lấy thẻ <div> to nhất
        main_div = soup.find('div')

        # # Lấy danh sách các thẻ con ngay sau thẻ <div> to nhất
        child_tags = [tag for tag in main_div.children if tag.name]


        #############################

        


        # # Tìm xem nó chương hay không
        # checkChuong = False
        # for tag in child_tags:  # child_tags là danh sách các thẻ con mà bạn đã lấy ra
        #     a_tags = tag.find_all("a", attrs={"name": re.compile(r"chuong_\d+(_\d+)?")})
        #     if len(a_tags) > 0:
        #         checkChuong = True
        #         break

        # # Tìm xem nó có mục hay không
        # checkMuc = False
        # for tag in child_tags:  # child_tags là danh sách các thẻ con mà bạn đã lấy ra
        #     a_tags = tag.find_all("a", attrs={"name": re.compile(r"muc_\d+(_\d+)?")})
        #     if len(a_tags) > 0:
        #         checkMuc = True
        #         break

        # # Tìm xem nó có điều 1. 2. 3. a) b) c) hay không
        # checkDieu = False
        # for tag in child_tags:  # child_tags là danh sách các thẻ con mà bạn đã lấy ra
        #     a_tags = tag.find_all("a", attrs={"name": re.compile(r"dieu_\d+(_\d+)?")})
        #     if len(a_tags) > 0:
        #         checkDieu = True
        #         break














        #############################
        # làm
        id = 1
        checkBegin = False   # để xem lúc nào thì bắt đầu lấy 
        current_title_Muc = ""
        current_title_Phan = ""
        # khi nào gặp điều, mục đầu tiên thì checkBegin  = True
        type = response.meta.get('type')
        id = response.meta.get('id')
        title = response.meta.get('title')
        href = response.meta.get('href')
        content = []  # để lưu content bộ


        checkBegin_Chuong = False
        id_Chuong = 1         
        title_Chuong = ''
        content_Chuong = []

        checkBegin_Muc = False
        id_Muc = 1         
        title_Muc = ''
        content_Muc = []

        checkBegin_Dieu = False
        id_Dieu = 1         
        title_Dieu = ''
        content_Dieu = ''

        # pattern1 = r"^Điều [A-Za-z0-9]+\."
        pattern2 = r"^Điều [A-Za-z0-9]+"
        # pattern2 = r"^\s\d+\.\s"  ## để lấy mấy cái điều mà chỉ có "12. Abc"
        # pattern3 = r"^\s*như[\r\n\s]*sau"

        
        # for index, tag in enumerate(child_tags, start=1):
        for i in range(int(len(child_tags))):
            tag = child_tags[i]

            if checkTableHead:
                if tag.name == "table":
                    cnt_table_begin = cnt_table_begin -1
                    print("đem:", cnt_table_begin)
                    print(i)
                    if cnt_table_begin >= 0:
                        continue
                    print(i)
                if cnt_table_begin > 0:
                    continue

            # nếu gặp table (chính là đoạn ký tên ở cuối thì dừng và add nốt vào re_article)
            if checkBegin: # chỉ check khi đã bắt đầu   
                # tìm xem có gặp table không
                # is_table = tag.find("table") is not None
                # if is_table:
                if tag.name == "table":
                    cnt_table = cnt_table -1
                if (tag.name == "table" and cnt_table == 0) or i == len(child_tags)-1:
                    # xử lý mấy cái có tiểu mục
                    if "tiểu mục" in title_Muc.lower():
                        title_Muc = current_title_Muc + " " + title_Muc
                    # nhét nốt điều vào mục
                    section_dict = {"id_Article": id_Dieu, "title_Article": title_Dieu, "content_Article": content_Dieu}
                    content_Muc.append(section_dict)
                    id_Dieu = id_Dieu + 1
                    title_Dieu = ''
                    content_Dieu = ''
                    # nhét mục vào chương
                    section_dict = {"id_Section": id_Muc, "title_Section": title_Muc, "content_Section": content_Muc}
                    content_Chuong.append(section_dict)
                    id_Muc = id_Muc + 1
                    title_Muc = ''
                    content_Muc = []
                    #
                    section_dict = {"id_Chapter": id_Chuong, "title_Chapter": title_Chuong, "content_Chapter": content_Chuong}
                    content.append(section_dict)
                    id_Chuong = id_Chuong + 1
                    title_Chuong = ''
                    content_Chuong = []
                    break

            




            ########## mấy cái ý to ở dưới chỉ là kiểm tra nó là thể loại nào và lấy text của nó
            # kiểm tra xem có phải chương không
            a_tags = tag.find_all("a", attrs={"name": re.compile(r"^chuong_\d+(_\d+)?$")})
            ## Nếu nó là chương
            if len(a_tags) > 0:
                # đôi khi cái tên chương nó viết hơi dài
                if checkBegin and checkBegin_Chuong:
                    pre_tag = child_tags[i-1]
                    if len(pre_tag.find_all("a", attrs={"name": re.compile(r"^chuong_\d+(_\d+)?$")})) > 0 or len(pre_tag.find_all("a", attrs={"name": re.compile(r"^chuong_\d+(_\d+)?_name$")})) > 0:
                        ### nếu k cộng thì ở dưới lại k kiểm tra đc
                        if title_Chuong.lower().startswith("phần"):
                            current_title_Phan = copy.deepcopy(title_Chuong)
                        title_Chuong = tag.get_text()
                        continue
                    
                    # thêm tên phần vào đằng trước nếu có 
                    if current_title_Phan != "":
                        title_Chuong = current_title_Phan + " " + title_Chuong

                    # nhét nốt câu vào điều trong trường hợp "mục" không xuất hiện
                    if content_Dieu != '' or title_Dieu != '':
                        section_dict = {"id_Article": id_Dieu, "title_Article": title_Dieu, "content_Article": content_Dieu}
                        content_Muc.append(section_dict)
                        id_Dieu = id_Dieu + 1
                        title_Dieu = ''
                        content_Dieu = ''
                    # nhét nốt mục vào chương hiện tại
                    # xử lý mấy cái có tiểu mục
                    if "tiểu mục" in title_Muc.lower():
                        title_Muc = current_title_Muc + " " + title_Muc
                    section_dict = {"id_Section": id_Muc, "title_Section": title_Muc, "content_Section": content_Muc}
                    content_Chuong.append(section_dict)
                    id_Muc = 1
                    title_Muc = ''
                    content_Muc = []
                    # nhét chương vào bộ
                    ### xử lý mấy cái "Phần thứ nhất..."
                    # if len(content_Chuong) == 1 and content_Chuong[0]["title_Section"] == "" and len(content_Chuong[0]["content_Section"]) == 0:
                    #     title_Chuong = title_Chuong + " " + tag.get_text()
                    #     continue
                        

                    section_dict = {"id_Chapter": id_Chuong, "title_Chapter": title_Chuong, "content_Chapter": content_Chuong}
                    content.append(section_dict)
                    id_Chuong = id_Chuong + 1
                    title_Chuong = ''
                    content_Chuong = []
                    # reset check begin mục bằng false, coi như làm lại từ chương mới
                    checkBegin_Muc = False
                    checkBegin_Dieu = False
                # tiếp tục với chuong
                title_Chuong = title_Chuong + tag.get_text()
                if title_Chuong.lower().startswith("phần"):
                    current_title_Phan = copy.deepcopy(title_Chuong)
                checkBegin = True
                checkBegin_Chuong = True
            # nếu là tên chương 
            elif len(tag.find_all("a", attrs={"name": re.compile(r"^chuong_\d+(_\d+)?_name$")})) > 0:
                title_Chuong = title_Chuong + " " + tag.get_text()

            #nếu không là chương
            else: 
                #####################################################
                ####### Ta làm lại y hệt như chương đối với mục #####
                #####################################################
                a_tags = tag.find_all("a", attrs={"name": re.compile(r"^muc_\d+(_\d+)?$")})
                ## Nếu nó là mục
                if len(a_tags) > 0:   ## and "mục" in tag.get_text().lower():
                    # nếu nó không phải là mục đầu tiên thì bắt đầu add vào re_article
                    if checkBegin and checkBegin_Muc:

                        pre_tag = child_tags[i-1]
                        if len(pre_tag.find_all("a", attrs={"name": re.compile(r"^muc_\d+(_\d+)?$")})) > 0:
                            ### nếu k cộng thì ở dưới lại k kiểm tra đc
                            if "tiểu mục" not in title_Muc.lower():
                                current_title_Muc = copy.deepcopy(title_Muc)
                            title_Muc = tag.get_text()
                            continue
                        
                        # xử lý mấy cái có tiểu mục
                        if "tiểu mục" in title_Muc.lower():
                            title_Muc = current_title_Muc + " " + title_Muc
                            

                        # nhét nốt điều vào mục
                        section_dict = {"id_Article": id_Dieu, "title_Article": title_Dieu, "content_Article": content_Dieu}
                        content_Muc.append(section_dict)
                        id_Dieu = id_Dieu + 1
                        title_Dieu = ''
                        content_Dieu = ''
                        # nhét mục vào chương
                        section_dict = {"id_Section": id_Muc, "title_Section": title_Muc, "content_Section": content_Muc}
                        content_Chuong.append(section_dict)
                        id_Muc = id_Muc + 1
                        title_Muc = ''
                        content_Muc = []
                        # reset check begin điều
                        checkBegin_Dieu = False
                    # tiếp tục với Muc
                    title_Muc = title_Muc + tag.get_text()
                    if "tiểu mục" not in title_Muc.lower():
                        current_title_Muc = copy.deepcopy(title_Muc)
                    checkBegin = True
                    checkBegin_Muc = True

                # nếu là tên mục 
                elif len(tag.find_all("a", attrs={"name": re.compile(r"^muc_\d+(_\d+)?_name$")})) > 0:
                    title_Muc = title_Muc + " " + tag.get_text()
                    if "tiểu mục" not in title_Muc.lower():
                        current_title_Muc = copy.deepcopy(title_Muc)

                #nếu không là mục
                else: 
                    #####################################################
                    ####### Ta làm lại y hệt như chương đối với điều #####
                    #####################################################
                    name_dieu = tag.get_text()
                    name_dieu = name_dieu.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("\t", " ")
                    if re.match(pattern2, name_dieu):
                        # nếu nó không phải là điều đầu tiên thì bắt đầu add vào re_article
                        if checkBegin and checkBegin_Dieu:
                            section_dict = {"id_Article": id_Dieu, "title_Article": title_Dieu, "content_Article": content_Dieu}
                            content_Muc.append(section_dict)
                            id_Dieu = id_Dieu + 1
                            title_Dieu = ''
                            content_Dieu = ''
                        # tiếp tục với Dieu
                        title_Dieu = title_Dieu + name_dieu
                        checkBegin = True
                        checkBegin_Dieu = True


                    #nếu không là điều
                    elif checkBegin: 
                        content_Dieu = content_Dieu + tag.get_text()


           

            

        item = LawItem()
        item["type"] = type
        item["id"] = id
        item["href"] = href
        item["title"] = title
        item["content"] = content
        yield item



