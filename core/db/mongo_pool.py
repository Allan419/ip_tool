from pymongo import MongoClient, ASCENDING, DESCENDING
import random

from settings import MONGODB_URL, MONGODB_DB_NAME, MONGODB_COLLECTION_NAME
from utils.log import logger
from domain import Proxy


class MongoPool(object):

    def __init__(self):
        self.client = MongoClient(MONGODB_URL)
        self.proxies = self.client[MONGODB_DB_NAME][MONGODB_COLLECTION_NAME]

    def __delattr__(self):
        self.client.close()

    def insert_one(self, proxy):
        # 使用proxy.ip作为mongodb的主键: _id
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info(f"向数据库 {self.proxies.full_name} 插入新代理 : {proxy.url()}")
        else:
            logger.warning(f"在数据库 {self.proxies.full_name} 已存在代理 : {proxy.url()}")

    def update_one(self, proxy):
        # 实现修改功能
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})
        logger.info(f"在数据库 {self.proxies.full_name} 更新代理 : {proxy.url()}")

    def delete_one(self, proxy):
        # 实现删除功能
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info(f"在数据库 {self.proxies.full_name} 删除代理 : {proxy.url()}")

    def find_all(self):
        cursor = self.proxies.find()
        for item in cursor:
            # 删除 '_id' 字段
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        """实现查询功能
        :param conditions: 查询条件字典
        :param count: 限制取出多少条代理IP
        :return: 满足条件的代理IP列表
        """
        cursor = self.proxies.find(conditions, limit=count).sort([
            ('score', DESCENDING), ('speed', ASCENDING)
        ])

        proxy_list = []
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)

        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        """根据 协议类型 和 要访问的网站的域名，获得代理IP列表
        :param protocol: 支持的协议 http https
        :param domain: 要访问网站的域名
        :param count: 用于限制获取多个代理IP, 默认是获取所有的
        :param nick_type: 匿名类型，默认获取高匿的IP
        :return: 满足条件的代理IP列表
        """
        # 定义查询条件
        conditions = {'nick_type': nick_type}
        if protocol is None:
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        else:
            conditions['protocal'] = {'$in': [1, 2]}

        if domain:
            conditions['disabled_domains'] = {'$nin': [domain]}
        # 返回满足要求的IP列表
        return self.find(conditions=conditions, count=count)

    def random_proxy(self, protocal=None, domain=None, nick_type=0, count=0):
        """返回满足要求的一个随机代理IP
        """
        try:
            proxy_list = self.get_proxies(protocol=protocal, domain=domain, count=count, nick_type=nick_type)
            return random.choice(proxy_list)
        except Exception as e:
            logger("当前没有满足要求的代理IP")

    def disable_domain(self, ip, domain):
        """实现把代理IP不可访问的域名添加到数据库中对应IP的disabled_domain字段中
        """
        if not self.proxies.count_documents({'_id': ip, 'disabled_domains': domain}):
            self.proxies.update_one({'_id': ip}, {'$push': {'disabled_domains': domain}})
            logger.info(f"将 {domain} 加入 {self.proxies.full_name}: {ip} 的 disabled_domains 字段 ")
        else:
            logger.info(f"此 {domain} 已在 {self.proxies.full_name}: {ip} 的 disabled_domains 字段 ")


if __name__ == '__main__':
    # proxy = Proxy('122.0.1.2','8900',protocol=2, speed=0.3, score = 50, disabled_domains=['jd.com', 'taobao.com'])
    # proxy = Proxy('4123.123.54.2','9000',protocol=1, speed=0.1, score = 49, disabled_domains=['jd.com'])
    # proxy = Proxy('112.5.2.6','8900',protocol=0, speed=0.5, score = 45, disabled_domains=['taobao.com'])
    # proxy = Proxy('11.2.12.5','8900',protocol=2, nick_type=0)

    mongo = MongoPool()
    # mongo.insert_one(proxy)
    # proxy = Proxy(ip='128.0.0.1',port='0008', nick_type=10)
    # mongo.update_one(proxy)
    print(mongo.random_proxy())

    # mongo.disable_domain('11.2.3.8','jd.com')
