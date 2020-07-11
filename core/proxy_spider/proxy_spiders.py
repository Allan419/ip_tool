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

class Vip7Spider(BaseSpider):
    """齐云代理Proxy IP爬虫   
    """
    urls = ['https://www.7yip.cn/free/?action=china&page={}'.format(i) for i in range(1,11)]
    group_xpath = "//*[@id='content']/section/div[2]/table/tbody/tr"
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }
    
class IP89Spider(BaseSpider):
    """89免费代理Proxy IP爬虫   
    """
    urls = ['http://www.89ip.cn/index_{}.html'.format(i) for i in range(1,11)]
    group_xpath = "//div/table[@class='layui-table']/tbody/tr"
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }

class IP3366Spider(BaseSpider):
    """云代理Proxy IP爬虫   
    """
    urls = ['http://www.ip3366.net/?stype={}&page={}'.format(i,j) for i in range(1,5) for j in range(1,11)]
    group_xpath = "//*[@id='list']/table/tbody/tr"
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[6]/text()'
    }

# class mimvp(BaseSpider):
    """云代理Proxy IP爬虫   
        https://proxy.mimvp.com/freeopen
        端口号为图片，需识别
    """
    
class KxDaiLiSpider(BaseSpider):
    """开心代理Proxy IP爬虫   
    """
    urls = ['http://www.kxdaili.com/dailiip/{}/{}.html'.format(i,j) for i in range(1,3) for j in range(1,10)]
    group_xpath = "//div/table[@class='active']/tbody/tr"
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[6]/text()'
    }

class JiangXianLiSpider(BaseSpider):
    """高可用全球免费代理IP库代理Proxy IP爬虫   
    """
    urls = ['https://ip.jiangxianli.com/?page={}'.format(i) for i in range(1,16)]
    group_xpath = "//div/table[@class='layui-table']/tbody/tr"
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[6]/text()'
    }

if __name__ == '__main__':
    kdl = JiangXianLiSpider()

    # print(help(XiLaDaiLiSpider))

    for proxy in kdl.get_proxies():
        print(proxy)

   