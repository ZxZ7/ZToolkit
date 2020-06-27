## An photo extractor for 500px
## NOTE: DO NOT USE FOR COMMERCIAL PURPOSES!!!

import re
from lxml import etree
from selenium import webdriver
import urllib.request
import time

def retrive_img(url, save_path):
    
    driver_path = r'D:\Python\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)

    driver.get(url)
    time.sleep(2)
    html = etree.HTML(driver.page_source)
    driver.quit()
    
    pic_url = html.xpath('//img[@class="photo-show__img"]/@src')[0]
    pic_num = re.findall('\/photo/(.*?)\/', pic_url)[0]
    pic_name = 'stock-photo-'+pic_num+'(1).jpg'
    
    urllib.request.urlretrieve(pic_url, save_path+pic_name)
    print('>> .\\'+pic_name+' saved.')


if __name__ == '__main__':

    url = input("Enter image URL:")
    save_path = r'./'
    retrive_img(url, save_path)
