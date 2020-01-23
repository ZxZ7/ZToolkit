import requests
from lxml import etree
import re
import pandas as pd



def get_detailURL(url, HEADERS, DOMAIN = 'https://www.dy2018.com'):
    '''
    Get URL of each movie page from a movie list.
    '''
    resp = requests.get(url, headers=HEADERS)
    # <META ...; charset=gb2312">
    text = resp.content.decode('gbk', errors='ignore')
    html = etree.HTML(text)
    
    # 每个table代表1个电影，找到每个电影页面的链接
    # <table ... class="tbspan">  <a href="/i/101650.html">
    detail_urls = html.xpath('//table[@class="tbspan"]//a/@href')
    detail_urls = map(lambda x: DOMAIN + x, detail_urls)
    
    return detail_urls



def parse_detailURL(url, HEADERS):
    '''
    Get detail movie infos on a movie page.
    '''
    resp = requests.get(url, headers=HEADERS)
    text = resp.content.decode('gbk', errors='ignore')
    html = etree.HTML(text)
    
    details = html.xpath("//div[@id='Zoom']//text()")  # 返回一个列表
    
    # 非常规页面
    if '◎上映日期' not in str(details):
        return None
    
    # 常规页面
    movie = {}
    for idx,info in enumerate(details):
        
        if info.startswith('◎主　　演'):  
            info = info.replace('◎', '')
            t = re.split('　', info)  # ['主', '', '演', '郑秀文']
            t = [t[0]+t[2], t[3]]     # ['主演', '郑秀文']

            # 获取全部主演：从该行的下一行开始，到下一个'◎'前结束
            for i in range(idx+1, len(details)):
                if details[i].startswith('◎'):
                    break
                t[1] = t[1] + ' ' + details[i].strip()  # strip()去空格
                # ['主演', '郑秀文 赖雅妍 李晓峰 钟镇涛 任贤齐 刘瑞琪 吴彦姝 刘德华']
            movie[t[0]] = t[1]
        
        # 除主演外的其他info，在简介前结束
        elif info.startswith('◎'):
            if info.startswith('◎简　　介'):
                break
            info = info.replace('◎', '')
            t = re.split('　', info)
            if len(t) == 4:
                t = [t[0]+t[2], t[3]]
            movie[t[0]] = t[1]
            
    download = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie['下载地址'] = download

    return movie
    


def movie_crawler(end_page, begin_page=1):
    '''
    begin_page, end_page: page number of movie lists
    '''
    url_all = []  # url of movie list pages
    if begin_page == 1:
        url1 = 'https://www.dy2018.com/html/gndy/dyzz/index.html'
        url_all.append(url1)
    
    # 第二页: "/html/gndy/dyzz/index_2.html"
    url_ = 'https://www.dy2018.com/html/gndy/dyzz/index_{}.html'
    for x in range(max(begin_page,2), end_page+1): # if end_page==1: range(2,2)
        url2_ = url_.format(x)
        url_all.append(url2_)

    
    movies = pd.DataFrame()
    i = 0
    for url in url_all:
        # 获取每页movie list中各个电影的detail urls
        detail_urls = get_detailURL(url)
        
        for detail_url in detail_urls:
            # 根据detail_url获取每个电影的详细信息
            movie = parse_detailURL(detail_url)            
            
            # 如不为空，则加入movies DataFrame
            if movie:
                movies[i] = pd.Series(movie)
                if i%5 == 0:
                    print('Movie count =', i+1)
                i += 1
    
    print('Movie count =', i)
    print('Done!')
    return movies.T





if __name__ == '__main__':
    movies = movie_crawler(1)
    print(movies.head(2))
    
