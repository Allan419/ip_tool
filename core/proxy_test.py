from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import schedule, time

from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from utils.log import logger
from settings import MAX_SCORE, PROXY_TEST_ASYNC_TASK_AMOUNT, PROXY_TEST_INTERVAL


class ProxyTest(object):

    def __init__(self):
        self.mongo_pool = MongoPool()
        # 创建Queue和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __modify_one_proxy(self, proxy):
        proxy = check_proxy(proxy)

        if proxy.speed == -1:
            proxy.score -= 1
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                self.mongo_pool.update_one(proxy)
        else:
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)

        return proxy

    def __check_callback(self, temp):
        self.coroutine_pool.apply_async(self.__execute_queued_task, callback=self.__check_callback)

    def __execute_queued_task(self):
        # 从Queue中获取一个代理IP
        proxy = self.queue.get()
        proxy = self.__modify_one_proxy(proxy)
        # 调用Queue的task done方法表示检测完毕一个代理IP
        self.queue.task_done()

    def __get_all_proxies_from_mongodb(self):
        return self.mongo_pool.find_all()

    def run(self):
        proxies = self.__get_all_proxies_from_mongodb()
        for proxy in proxies:
            # 把代理IP添加到Queue中
            self.queue.put(proxy)
            # self.__modify_one_proxy(proxy)

        # 开启多个异步任务，开始数量有settings设置
        for i in range(PROXY_TEST_ASYNC_TASK_AMOUNT):
            # 开始协程池进行单线程异步任务
            self.coroutine_pool.apply_async(self.__execute_queued_task, callback=self.__check_callback)
        # 让当前线程等待队列任务的完成
        self.queue.join()

    @classmethod
    def start(cls):
        pt = cls()
        pt.run()
        logger.info('*****************本次检测完毕，等待下次检测*****************')
        schedule.every(PROXY_TEST_INTERVAL).minutes.do(pt.run)
        while True:
            # print("等待下次更新")
            schedule.run_pending()
            # time.sleep(PROXY_TEST_INTERVAL * 60 /2 + 1)
            time.sleep(1)


if __name__ == '__main__':
    ProxyTest.start()
