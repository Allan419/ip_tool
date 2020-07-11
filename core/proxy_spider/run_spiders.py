# 想使用携程池，首先打猴子补丁
from gevent import monkey
monkey.patch_all()
# 导入携程池
from gevent.pool import Pool

import importlib, schedule
import time

from settings import PROXY_SPIDERS, RUN_SPIDERS_INTERVAL
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger

class RunSpider(object):

    def __init__(self):
        self.mongo_pool = MongoPool()
        # 创建携程池对象
        self.coroutine_pool = Pool()

    def get_spiders_from_settings(self):
        for spider_full_path in PROXY_SPIDERS:
            module_name, class_name = spider_full_path.rsplit('.', maxsplit=1)
            # 根据已经获得的module_name动态导入模块
            module = importlib.import_module(module_name)
            # 根据类名，从模块中获取类
            cls = getattr(module, class_name)
            # 创建爬虫对象
            spider = cls()
            yield spider

    def __execute_one_spider_task(self, spider):
        try:
            for proxy in spider.get_proxies():
                # 检测代理IP可用性
                proxy = check_proxy(proxy)
                # print(proxy)
                # 如果可用就入数据库
                if proxy.speed != -1:
                    self.mongo_pool.insert_one(proxy)
        except Exception as e:
            logger.exception(e)

    def run(self):
        spiders = self.get_spiders_from_settings()
        for spider in spiders:
            self.coroutine_pool.apply_async(self.__execute_one_spider_task, args=(spider, ))
            # self.__execute_one_spider_task(spider)
        self.coroutine_pool.join()

    # 定时调用run方法启动spiders
    @classmethod
    def start(cls):
        r = RunSpider()
        r.run()
        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(r.run)
        while True:
            schedule.run_pending()
            time.sleep(RUN_SPIDERS_INTERVAL*60*60/2+1)

if __name__ == '__main__':
    RunSpider.start()