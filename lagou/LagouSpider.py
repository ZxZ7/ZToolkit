from selenium import webdriver
from lxml import etree
import re
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LagouSpider:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url 
        self.positions = []        
        
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source # 获取ajax数据
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@action='next']"))
            )
            
            self.parse_list(source)
            
            try:     # 红包弹窗
                body_bg = self.driver.find_element_by_xpath("//div[@class='body-btn']")
                body_bg.click()
                time.sleep(1)
            finally: # 下一页
                next_btn = self.driver.find_element_by_xpath("//span[@action='next']")
                if 'pager_next_disabled' in next_btn.get_attribute('class'):
                    break
                else:
                    next_btn.click()
                time.sleep(1)
            
            
    def parse_list(self, source):
        html = etree.HTML(source)
        links = html.xpath('//a[@class="position_link"]/@href')
        for link in links:
            self.request_detail(link)
            time.sleep(1)

            
    def request_detail(self, link):
        # 打开并切换到新页面
        self.driver.execute_script("window.open('%s')"%link)
        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "job-name"))
        )
        
        source = self.driver.page_source
        self.parse_detail(source)
        # 关闭当前页面，并切换回列表页
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        
    def parse_detail(self, source):
        html = etree.HTML(source)
        
        position = {}
        position['title'] = html.xpath("//div[@class='job-name']/@title")[0].strip()
        position['company'] = html.xpath("//h4[@class='company']/text()")[0].strip()
        
        job_requests = html.xpath("//dd[@class='job_request']//span")
        for idx, request in enumerate(['salary', 'city', 'exp', 'edu', 'type']):
            text = job_requests[idx].xpath('.//text()')[0]
            text = re.sub(r'[\s/]', '', text) # 去"/"去空格
            position[request] = text
        
        desc = html.xpath("//div[@class='job-detail']//text()") # 包含多个字符串的列表
        desc_str = ''
        for line in desc:
            desc_str += line
        desc_str = re.sub(r'[\s]', '', desc_str)
        position['desc'] = desc_str
        
#         print(position)
        self.positions.append(position)        
        
        

if __name__ == '__main__':
    driver_path = r' '
    driver = webdriver.Chrome(executable_path=driver_path)
    url = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90\
    %E5%B8%88/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
    spider = LagouSpider(url, driver)
    spider.run()
    
    # save as csv
    headers = spider.positions[0].keys()
    with open('positions.csv', 'w', encoding='utf_8_sig', newline='') as fp:
        writer = csv.DictWriter(fp, headers)
        writer.writeheader()
        writer.writerows(spider.positions)
