import scrapy
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy_demo.lagou.lagou.items import LagouItem
from lxml import etree

class LagouSpiderSpider(scrapy.Spider):
    name = 'lagou_spider'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"D:\programs\chrome_driver\chromedriver.exe")
        self.start_page = 1
        self.start_num = 1

    # 主解析
    def parse(self, response):
        # 处理登录页面
        self.process_login(response.url) # print("登录处理结束")
        page = 1

        # 控制不断向下点击
        while True:
            # 当页数小于预定值
            num = 1
            if self.start_page <= page :
                # 循环遍历列表
                page_source = self.driver.page_source
                time.sleep(1)
                source = etree.HTML(page_source)
                position_list = self.parse_page(source)  # 职位列表
                # 解析详细页面
                for position in position_list:

                    if self.start_page == page and num < self.start_num:
                        num += 1
                        continue
                    else:
                        source = self.pre_parse_job(position)
                        item = self.parse_job(source)  # 要有返回值item，这个item在这里yield

                        print("正在爬取第{}页第{}个数据".format(page, num))
                        num = num + 1
                        yield item

            # 获取下一页按钮
            next_page = self.get_nextpage()
            if next_page.get_attribute("class") == "pager_next ":
                next_page.click()
                page = page + 1
                time.sleep(1)
            else:
                break

    # 登录
    def process_login(self,url):
        """处理登录页面"""
        # print("处理登录页面")
        self.driver.get(url)
        time.sleep(0.5)
        # 发送请求前的操作
        close_button = self.driver.find_element_by_xpath("//*[@id='cboxClose']")
        close_button.click()
        time.sleep(0.5)
        serch_text = self.driver.find_element_by_xpath("//*[@id='search_input']")
        # print(serch_text)
        serch_text.send_keys("java")
        submit_button = self.driver.find_element_by_xpath("//*[@id='search_button']")
        submit_button.click()
        time.sleep(0.5)
        close_button1 = self.driver.find_element_by_xpath("/html/body/div[9]/div/div[2]")
        close_button1.click()
        time.sleep(0.5)

    # 解析列表
    def parse_page(self,source):

        """工作列表解析"""
        position_list = []
        li_list = source.xpath("/html/body/div[7]/div[2]/div[1]/div[3]/ul/li")
        # 获取所有职位详细地址
        for li in li_list:
            # print("li:",li)
            href = li.xpath("./div[1]/div[1]/div[1]/a/@href")[0].split("?")[0]
            position_list.append(href)
        return position_list

    # 解析职位
    def parse_job(self,source):
        """工作详情页解析"""

        company_name = source.xpath("//*[@id='job_company']/dt/a/div/h3/em/text()")[0].strip()

        #
        company_field = source.xpath("//*[@id='job_company']/dd//h4[@class='c_feature_name']//text()")[
            0].strip()
        # print(company_field)
        #

        company_stage = source.xpath("//*[@id='job_company']//dd//li/h4[@class='c_feature_name']//text()")[1:-1]
        company_stage = "".join(company_stage)

        company_size = source.xpath("//*[@id='job_company']/dd/ul//li/h4[@class='c_feature_name']//text()")[-1]
        company_size = "".join(company_size)

        company_website = source.xpath("//*[@id='job_company']//dd//a//h4[@class='c_feature_name']/text()")[
            0].strip()
        # print(company_website)

        job_name = source.xpath("/html/body//div//div/h1[@class='name']/text()")[0].strip()
        # print(job_name)
        job_salary = source.xpath("/html/body/div[7]/div/div[1]/dd/h3/span[@class='salary']/text()")[0].strip()
        job_tempt = source.xpath("//*[@id='job_detail']/dd[1]/p/text()")[0].strip()
        job_overlook = source.xpath("/html/body/div[7]/div/div[1]/dd/h3//text()")
        job_overlook = "".join(job_overlook)
        job_descript = source.xpath("//*[@id='job_detail']//dd//text()")
        job_descript = "".join(job_descript)
        job_location = source.xpath("//*[@id='job_detail']//dd//div[@class='work_addr']//text()")
        job_location = "".join(job_location).strip()
        item = LagouItem(company_name=company_name, company_field=company_field, company_stage=company_stage,
                         company_website=company_website, company_size=company_size,
                         job_salary=job_salary, job_descript=job_descript, job_location=job_location,
                         job_name=job_name, job_overlook=job_overlook, job_tempt=job_tempt)

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(0.3)
        # print(item)
        return item

    # 解析职位之前的操作
    def pre_parse_job(self,position):
        # 控制页面切换
        self.driver.execute_script("window.open('" + position + "')")
        time.sleep(0.5)
        try:
            self.driver.set_page_load_timeout(3)
        except:
            # js刷新页面
            print("js来刷新一下页面")
            self.driver.execute_script("location.reload()")

        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(0.3)
        # 判断页面的加载情况

        try:
            next_page = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located
                                                            ((By.XPATH,
                                                              "/html/body/div[7]/div/div[1]")))
            # print(next_page)
        except:
            print("没有加载成功")

        page_source = self.driver.page_source
        time.sleep(0.2)
        source = etree.HTML(page_source)
        # 将页面静态代码给函数处理
        # print("正在爬取第{}页第{}个数据".format(page, num))
        return source

    # 获取下一页按钮
    def get_nextpage(self):
        try:
            next_page = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located
                                                             ((By.XPATH,
                                                               "/html/body/div[7]/div[2]/div[1]/div[3]/div[2]/div/span[last()]")))
            # print(next_page)
        except:
            print("没有下一页了或者没有加载成功")
        return next_page
            # 判断是否还有下一页





