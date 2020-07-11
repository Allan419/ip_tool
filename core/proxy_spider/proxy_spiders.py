import random

from base_spider import BaseSpider

class KuaiDaiLiSpider(BaseSpider):
    """快代理Proxy IP爬虫   
    """
    urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1,11)]
    group_xpath = "//*[@id='list']/table/tbody/tr"
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }
    # 随机设置爬虫爬取每个页面的间隔时间 1-3秒
    # def __init__(self):
    #     super().__init__()
    #     self.pause = random.uniform(1,3)


class XiLaDaiLiSpider(BaseSpider):
    """西拉代理Proxy IP爬虫   
    """
    urls = ['http://www.xiladaili.com/gaoni/{}/'.format(i) for i in range(1,11)]
    group_xpath = "/html/body/div/div[3]/div[2]/table/tbody/tr"
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[1]/text()',
        'area': './td[4]/text()'
    }
    # 随机设置爬虫爬取每个页面的间隔时间 1-3秒
    # def get_page_from_url(self, url):
    #     time.sleep(random.uniform(1, 3))
    #     return super().get_page_from_url(url)
    
# class IP66(BaseSpider):

    

if __name__ == '__main__':
    kdl = XiLaDaiLiSpider()

    # print(help(XiLaDaiLiSpider))

    for proxy in kdl.get_proxies():
        print(proxy)

   