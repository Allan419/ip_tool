
import requests, time, re, random
from lxml import etree

from utils.http import get_request_headers
from domain import Proxy
from utils.log import loggerProxySpider

IP_PATTERN = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
PORT_PATTERN = re.compile('\d{1,5}$')

class BaseSpider(object):
    """通用爬虫类  
    :param urls: 要抓取代理IP的网页列表  
    :param group_xpath: 分组的XPATH, 用于抓取页面中包含代理IP的标签列表  
    :param detail_xpath: 组内的XPATH, 用于提取 IP, PORT, AREA  
    :param pause: 抓取间隔，防止返回<Response 503>  
    """
    # urls = []
    # group_xpath = ''
    # detail_xpath = {}
    # pause = 0

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        # 发送URL请求，返回响应
        headers = get_request_headers()
        # print(user_agent)
        response = requests.get(url, headers=headers)
        pause = random.uniform(1, 3)
        time.sleep(pause)
        loggerProxySpider.info(f"Request for {url} returned {response}. Pause for {pause} seconds")
        return response.content

    def get_first_from_list(self, _list):
        # 如果列表中有元素就返回第一个，否则返回空串
        return _list[0] if len(_list) != 0 else ''

    def get_proxies_from_page(self, page):
        # 解析页面,提取数据并封装成Proxy对象
        element = etree.HTML(page)
        # 获取包含代理IP信息的标签列表
        trs = element.xpath(self.group_xpath)
        for tr in trs:
            ip = IP_PATTERN.search(self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))).group()
            port = PORT_PATTERN.search(self.get_first_from_list(tr.xpath(self.detail_xpath['port']))).group()
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))

            proxy = Proxy(ip=ip, port=port, area=area)
            yield proxy

    def get_proxies(self):
        # 获取代理IP
        for url in self.urls:
            page = self.get_page_from_url(url)
            proxies = self.get_proxies_from_page(page)
            yield from proxies

# if __name__ == '__main__':

#     url = ['https://www.kuaidaili.com/free/']
#     group_xpath = "//*[@id='list']/table/tbody/tr"
#     detail_xpath = {
#         'ip': './td[1]/text()',
#         'port': './td[2]/text()',
#         'area': './td[5]/text()'
#     }
    

#     bs = BaseSpider(url, group_xpath, detail_xpath)
#     print(bs.get_proxies())
#     for proxy in bs.get_proxies():
#          print(proxy)
   



